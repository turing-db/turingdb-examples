import argparse
import csv
import resource
import socket
import subprocess
import sys
import time

from turingdb import TuringDB

import ollama


TURINGDB_PORT = 1234
TURINGDB_HOST = "localhost"
DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"

AVAILABLE_MODELS = [
    "snowflake-arctic-embed:33m",
    "snowflake-arctic-embed:110m",
    "all-minilm:22m",
    "all-minilm:33m",
    "nomic-embed-text",
    "mxbai-embed-large",
]

DIMENSIONS = {
    "snowflake-arctic-embed:33m": 384,
    "snowflake-arctic-embed:110m": 768,
    "all-minilm:22m": 384,
    "all-minilm:33m": 384,
    "nomic-embed-text": 768,
    "mxbai-embed-large": 1024,
}

CONTEXT_WINDOWS = {
    "snowflake-arctic-embed:33m": 512,
    "snowflake-arctic-embed:110m": 512,
    "all-minilm:22m": 512,
    "all-minilm:33m": 512,
    "nomic-embed-text": 2048,
    "mxbai-embed-large": 512,
}

assert all(m in AVAILABLE_MODELS for m in DIMENSIONS.keys())
assert all(m in AVAILABLE_MODELS for m in CONTEXT_WINDOWS.keys())


def is_port_open(host: str, port: int) -> bool:
    try:
        sock = socket.create_connection((host, port), timeout=1)
        sock.close()
        return True
    except OSError:
        return False


def wait_port(host: str, port: int, timeout: float = 60.0) -> bool:
    """Wait until TCP port accepts connections. Returns True on success, False on timeout."""
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        if is_port_open(host, port):
            return True

        time.sleep(0.5)

    return False


def _raise_fd_limit() -> None:
    """Raise the open-file-descriptor limit to the OS hard maximum."""
    _, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))


def start_turingdb() -> subprocess.Popen:
    print(f"Starting turingdb on port {TURINGDB_PORT}...")
    return subprocess.Popen(
        [
            "uv",
            "run",
            "turingdb",
            "-demon",
            "-load",
            "reactome",
            "-p",
            str(TURINGDB_PORT),
        ],
        preexec_fn=_raise_fd_limit,
    )


def ensure_turingdb_running() -> subprocess.Popen | None:
    """Start turingdb if not already running. Returns the process if we started it, else None."""
    if is_port_open(TURINGDB_HOST, TURINGDB_PORT):
        print("turingdb is already running.")
        return None

    process = start_turingdb()
    print("Waiting for turingdb to be ready...")
    if not wait_port(TURINGDB_HOST, TURINGDB_PORT, timeout=60):
        process.terminate()
        print("ERROR: Timed out waiting for turingdb to start.", file=sys.stderr)
        sys.exit(1)

    print("turingdb is ready.")
    return process


def get_node_id(node: dict) -> str:
    for key in ("id", "_id", "nodeId", "node_id"):
        if key in node:
            return str(node[key])
    raise ValueError(f"Cannot determine node ID from: {node}")


def cmd_build(
    client: TuringDB, embedder: ollama.Ollama, args: argparse.Namespace
) -> None:
    dim = DIMENSIONS[args.model]
    if args.clean:
        try:
            client.query("DELETE VECTOR INDEX reactome_index")
            print("Deleted existing vector index.")
        except Exception:
            pass  # Index did not exist — that is fine
        client.query(
            f"CREATE VECTOR INDEX reactome_index WITH DIMENSION {dim} METRIC COSINE"
        )
        print("Created vector index.")

    print("Fetching nodes with text property...")
    result = client.query(
        "MATCH (n) WHERE n.text IS NOT NULL AND n.dbId IS NOT NULL RETURN n.dbId, n.text"
    )
    total = len(result)
    print(f"Computing embeddings for {total} nodes...")

    context = CONTEXT_WINDOWS[args.model]

    with open("/home/ubuntu/.turing/data/vectors.csv", "w", newline="") as f:
        writer = csv.writer(f)
        ns = result["n.dbId"]
        texts = result["n.text"]
        batch_size = args.batch_size
        skipped = 0
        for start in range(0, total, batch_size):
            end = min(start + batch_size, total)
            # Filter out rows where text is None/empty; truncate to context limit
            pairs = [
                (ns[i], str(texts[i])[:context])
                for i in range(start, end)
                if texts[i] is not None and str(texts[i]).strip()
            ]
            skipped += (end - start) - len(pairs)
            if not pairs:
                continue
            batch_ids, batch_texts = zip(*pairs)
            embeddings = embedder.embed_batch(list(batch_texts))
            for node_id, embedding in zip(batch_ids, embeddings):
                writer.writerow([node_id, *embedding])
        if skipped:
            print(f"  (skipped {skipped} nodes with null/empty text)")
            print(f"  {end}/{total} nodes processed...")

    print("Loading vectors into index...")
    client.query('LOAD VECTOR FROM "vectors.csv" IN reactome_index')
    print("Index populated successfully.")


def cmd_query(
    client: TuringDB, embedder: ollama.Ollama, args: argparse.Namespace
) -> None:
    extra_queries = embedder.expand_query(args.text)
    all_queries = [args.text] + extra_queries
    print(
        f"Running search with {len(all_queries)} quer{'y' if len(all_queries) == 1 else 'ies'}:"
    )
    for q in all_queries:
        print(f"  - {q!r}")

    seen_ids: set[str] = set()
    rows: list[dict] = []
    for query in all_queries:
        embedding = embedder.embed(query)
        vector_literal = ", ".join(str(v) for v in embedding)
        result = client.query(f"""
            VECTOR SEARCH IN reactome_index FOR {args.top_k} [{vector_literal}] YIELD ids
            MATCH (n) WHERE n.dbId = ids RETURN n.dbId, n.displayName, n.text
            """)
        for i in range(result.shape[0]):
            db_id = str(result["n.dbId"][i])
            if db_id not in seen_ids:
                seen_ids.add(db_id)
                rows.append(
                    {
                        "dbId": db_id,
                        "displayName": result["n.displayName"][i],
                        "text": result["n.text"][i],
                    }
                )

    print(f"Re-ranking {len(rows)} candidates...")
    from sentence_transformers import CrossEncoder

    cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    pairs = [(args.text, row["text"]) for row in rows]
    scores = cross_encoder.predict(pairs)
    rows = [
        row for _, row in sorted(zip(scores, rows), key=lambda x: x[0], reverse=True)
    ]

    top_rows = rows[: args.top_k]

    template_res = """
        ==========
        Node name : {displayName}
        Node id   : {dbId}
        ----------
        {text}
        ==========
    """
    for row in top_rows:
        print(template_res.format(**row))

    print("\n" + "=" * 60)
    print("Generating answer from context...")
    answer = embedder.query_with_context(args.text, top_rows)
    print(answer)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reactome vector index builder and searcher backed by turingdb + ollama"
    )
    parser.add_argument(
        "--model",
        default="all-minilm:33m",
        choices=AVAILABLE_MODELS,
        help=("Embedding model to use (default: %(default)s). "),
    )
    parser.add_argument(
        "--ollama-url",
        default=DEFAULT_OLLAMA_URL,
        help="Base URL of the Ollama API (default: %(default)s)",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete and recreate the vector index before populating (build mode only)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=64,
        help="Number of texts sent to ollama per /api/embed request (default: %(default)s)",
    )

    subparsers = parser.add_subparsers(dest="command")

    # query subcommand
    query_parser = subparsers.add_parser("query", help="Search the vector index")
    query_parser.add_argument("text", help="Natural-language query to embed and search")
    query_parser.add_argument(
        "--top-k",
        type=int,
        default=20,
        help="Number of nearest neighbours to return (default: %(default)s)",
    )

    args = parser.parse_args()

    print(f"Pulling model '{args.model}' from Ollama...")
    subprocess.run(["ollama", "pull", args.model], check=True)

    embedder = ollama.Ollama(args.model, args.ollama_url)

    process = ensure_turingdb_running()
    client = TuringDB(host=f"http://{TURINGDB_HOST}:{TURINGDB_PORT}")
    client.set_graph("reactome")

    try:
        if args.command == "query":
            cmd_query(client, embedder, args)
        else:
            # Default: build / populate
            cmd_build(client, embedder, args)
    finally:
        if process is not None:
            process.terminate()
            process.wait()


if __name__ == "__main__":
    main()

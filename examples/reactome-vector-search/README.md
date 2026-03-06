# Reactome Vector Search

Semantic search over the [Reactome](https://reactome.org/) biological pathway knowledge graph, powered by [TuringDB](https://github.com/turing-db/turingdb) vector indexes and [Ollama](https://ollama.com/) embedding models.

## How it works

1. **Build** — nodes with a `text` property are fetched from the Reactome graph, embedded via an Ollama embedding model, and loaded into a TuringDB vector index.
2. **Query** — a natural-language question is expanded into multiple rephrased variants (using `qwen2.5:3b`), each variant is embedded and searched against the index, results are re-ranked with a cross-encoder, and a final answer is generated using `qwen2.5:3b` with the top retrieved passages as context.

## Prerequisites

### 1. Reactome data in TuringDB

You need the Reactome dataset available as a TuringDB graph named `reactome`. Follow the loading instructions in the [turing-bench repository](https://github.com/turing-db/turing-bench/).

### 2. Ollama

Install [Ollama](https://ollama.com/) and make sure it is running:

```bash
ollama serve
```

The script will automatically pull the selected embedding model. You also need the generation/query-expansion model:

```bash
ollama pull qwen2.5:3b
```

### 3. Python dependencies

```bash
uv sync
```

## Usage

### Build the vector index

```bash
uv run python main.py
```

This fetches all Reactome nodes that have a `text` property, computes embeddings, and loads them into a TuringDB vector index called `reactome_index`.

To rebuild from scratch (drop and recreate the index first):

```bash
uv run python main.py --clean
```

### Query the index

```bash
uv run python main.py query "Give me information on the apoptosis signaling pathway"
```

The query command:
- Expands the question into 3 semantically similar variants
- Embeds all variants and retrieves candidates from the vector index
- Re-ranks results with a cross-encoder (`cross-encoder/ms-marco-MiniLM-L-6-v2`)
- Prints the top-k nodes and generates a RAG answer

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--model` | `all-minilm:33m` | Ollama embedding model to use |
| `--ollama-url` | `http://127.0.0.1:11434` | Base URL of the Ollama API |
| `--clean` | off | Drop and recreate the vector index before building |
| `--batch-size` | `64` | Texts per Ollama `/api/embed` request |
| `--top-k` | `20` | Number of nearest neighbours to retrieve (query mode) |

### Hard-coded embedding models

| Model | Dimensions | Context window |
|-------|-----------|----------------|
| `all-minilm:22m` | 384 | 512 |
| `all-minilm:33m` | 384 | 512 |
| `snowflake-arctic-embed:33m` | 384 | 512 |
| `snowflake-arctic-embed:110m` | 768 | 512 |
| `nomic-embed-text` | 768 | 2048 |
| `mxbai-embed-large` | 1024 | 512 |

import sys

import requests


class Ollama:
    def __init__(self, model: str, base_url: str = "http://127.0.0.1:11434") -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")

    def _post(self, input: str | list[str]) -> list[list[float]]:
        response = requests.post(
            f"{self.base_url}/api/embed",
            json={"model": self.model, "input": input},
            timeout=300,
        )
        if response.status_code == 404:
            print(
                f"ERROR: ollama returned 404 for model '{self.model}'. "
                f"Pull it first with: ollama pull {self.model}",
                file=sys.stderr,
            )
            sys.exit(1)
        if not response.ok:
            print(
                f"ERROR: ollama {response.status_code}: {response.text}",
                file=sys.stderr,
            )
            response.raise_for_status()
        return response.json()["embeddings"]

    def embed(self, text: str) -> list[float]:
        return self._post(text)[0]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return self._post(texts)

    def query_with_context(
        self, query: str, results: list[dict], gen_model: str = "qwen2.5:3b"
    ) -> str:
        """Answer *query* using *results* as context via the given Ollama model."""
        from . import build_rag_prompt, enforce_sources
        prompt = build_rag_prompt(query, results)
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={"model": gen_model, "prompt": prompt, "stream": False},
            timeout=300,
        )
        response.raise_for_status()
        return enforce_sources(response.json()["response"], results)

    def expand_query(self, query: str, expand_model: str = "qwen2.5:3b") -> list[str]:
        """Return up to 3 rephrased variants of *query* for multi-query search.

        On JSON parse failure prints an error and returns an empty list so the
        caller can fall back to the original query only.
        """
        import json

        prompt = (
            "Rephrase the following search query into 3 different but semantically "
            "similar queries that could retrieve the same information from a biological "
            "pathway database. Respond with valid JSON only, in this exact format:\n"
            '{"queries": ["<query1>", "<query2>", "<query3>"]}\n\n'
            f"Original query: {query}"
        )
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={"model": expand_model, "prompt": prompt, "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        raw = response.json()["response"]
        try:
            return json.loads(raw)["queries"]
        except Exception:
            print(f"ERROR: could not parse LLM response as JSON:\n{raw}", file=sys.stderr)
            return []

"""Vector embeddings for semantic search (via Ollama)."""
import requests
from typing import Optional

class EmbeddingsClient:
    """Connect to Ollama for nomic-embed-text."""

    def __init__(self, base_url: str = "http://localhost:11434") -> None:
        self.base_url = base_url
        self.model = "nomic-embed-text"

    def embed(self, text: str) -> Optional[list[float]]:
        """Get embedding for text."""
        try:
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json={"model": self.model, "prompt": text},
                timeout=10
            )
            return response.json().get("embedding")
        except Exception as e:
            print(f"Embedding error: {e}")
            return None

    def semantic_search(self, query: str, corpus: list[str], k: int = 5) -> list[int]:
        """Find top-k most similar docs."""
        query_emb = self.embed(query)
        if not query_emb:
            return []

        corpus_embs = [self.embed(doc) or [] for doc in corpus]
        scores = [
            sum(q * c for q, c in zip(query_emb, doc_emb))
            for doc_emb in corpus_embs
        ]
        return sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]

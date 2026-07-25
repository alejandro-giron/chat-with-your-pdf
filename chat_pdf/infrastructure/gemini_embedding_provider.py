from __future__ import annotations

from typing import List, Any


class GeminiEmbeddingProvider:
    """Concrete embedding provider using the Google GenAI client."""

    def __init__(self, client: Any, model_name: str = "gemini-embedding-001") -> None:
        self.client = client
        self.model_name = model_name

    def embed(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            raise ValueError("texts must not be empty")

        response = self.client.models.embed_content(
            model=self.model_name,
            contents=texts,
        )

        embeddings = response.get("embeddings", [])
        return [embedding.get("values", []) for embedding in embeddings]

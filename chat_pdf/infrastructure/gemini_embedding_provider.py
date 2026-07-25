from __future__ import annotations

from typing import Any, List


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

        if hasattr(response, "embeddings"):
            embeddings = response.embeddings
        elif isinstance(response, dict):
            embeddings = response.get("embeddings", [])
        else:
            embeddings = []

        if hasattr(embeddings, "__iter__") and not isinstance(embeddings, (str, bytes)):
            normalized_embeddings: List[List[float]] = []
            for embedding in embeddings:
                if isinstance(embedding, dict):
                    values = embedding.get("values", embedding.get("embedding", []))
                else:
                    values = getattr(embedding, "values", None)
                    if callable(values):
                        values = None

                if values is None:
                    values = embedding

                if isinstance(values, (list, tuple)):
                    normalized_embeddings.append(list(values))
                elif hasattr(values, "__iter__") and not isinstance(values, (str, bytes)):
                    normalized_embeddings.append(list(values))
                else:
                    normalized_embeddings.append([])

            return normalized_embeddings

        return []

from __future__ import annotations

from typing import List, Protocol


class EmbeddingProvider(Protocol):
    def embed(self, texts: List[str]) -> List[List[float]]:
        """Return embeddings for the provided texts."""


class EmbeddingService:
    """Wrap an embedding provider with simple validation and convenience methods."""

    def __init__(self, provider: EmbeddingProvider) -> None:
        self.provider = provider

    def embed(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            raise ValueError("texts must not be empty")

        return self.provider.embed(texts)

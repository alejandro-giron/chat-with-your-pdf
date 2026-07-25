from typing import List

import pytest

from chat_pdf.services.embedding_service import EmbeddingService


class FakeEmbeddingProvider:
    def embed(self, texts: List[str]) -> List[List[float]]:
        return [[float(len(text))] for text in texts]


def test_embedding_service_returns_embeddings_for_texts() -> None:
    provider = FakeEmbeddingProvider()
    service = EmbeddingService(provider)

    embeddings = service.embed(["hello", "world"])

    assert embeddings == [[5.0], [5.0]]


def test_embedding_service_raises_for_empty_input() -> None:
    provider = FakeEmbeddingProvider()
    service = EmbeddingService(provider)

    with pytest.raises(ValueError):
        service.embed([])

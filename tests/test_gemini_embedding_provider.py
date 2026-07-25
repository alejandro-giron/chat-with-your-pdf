from typing import List

import pytest

from chat_pdf.infrastructure.gemini_embedding_provider import GeminiEmbeddingProvider


class DummyClient:
    def __init__(self) -> None:
        self.calls: List[List[str]] = []

    class Models:
        def __init__(self, parent: "DummyClient") -> None:
            self.parent = parent

        def embed_content(self, *, model: str, contents: List[str]) -> dict:
            self.parent.calls.append(contents)
            return {"embeddings": [{"values": [0.1, 0.2, 0.3]} for _ in contents]}

    @property
    def models(self) -> "DummyClient.Models":
        return DummyClient.Models(self)


def test_gemini_embedding_provider_returns_embeddings() -> None:
    client = DummyClient()
    provider = GeminiEmbeddingProvider(client=client, model_name="test-model")

    embeddings = provider.embed(["hello", "world"])

    assert embeddings == [[0.1, 0.2, 0.3], [0.1, 0.2, 0.3]]
    assert client.calls == [["hello", "world"]]


def test_gemini_embedding_provider_raises_for_empty_input() -> None:
    provider = GeminiEmbeddingProvider(client=DummyClient(), model_name="test-model")

    with pytest.raises(ValueError):
        provider.embed([])

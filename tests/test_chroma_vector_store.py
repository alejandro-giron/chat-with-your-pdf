import importlib

import numpy as np

import chat_pdf.infrastructure.chroma_vector_store as chroma_module


class FakeCollection:
    def __init__(self, existing_embeddings=None, raise_on_mismatch=False) -> None:
        self.existing_embeddings = existing_embeddings or []
        self.added_documents = []
        self.raise_on_mismatch = raise_on_mismatch

    def count(self) -> int:
        return len(self.existing_embeddings)

    def get(self, include=None):
        return {"embeddings": self.existing_embeddings}

    def add(self, documents, embeddings, ids):
        if self.raise_on_mismatch and self.existing_embeddings and embeddings and len(embeddings[0]) != len(self.existing_embeddings[0]):
            raise ValueError("Collection expecting embedding with dimension of 3072, got 384")
        self.existing_embeddings = [list(embedding) for embedding in embeddings]
        self.added_documents.append((documents, embeddings, ids))


class FakeClient:
    def __init__(self) -> None:
        self.collections = {}
        self.deleted = []

    def get_or_create_collection(self, name):
        if name not in self.collections:
            self.collections[name] = FakeCollection()
        return self.collections[name]

    def delete_collection(self, name):
        self.deleted.append(name)
        self.collections[name] = FakeCollection()


def test_chroma_vector_store_recreates_collection_when_embedding_dimension_changes(monkeypatch) -> None:
    client = FakeClient()
    existing_collection = FakeCollection(existing_embeddings=[[0.0] * 3072], raise_on_mismatch=True)
    client.collections["pdf_documents"] = existing_collection

    monkeypatch.setattr(chroma_module.chromadb, "PersistentClient", lambda path=None: client)

    store = chroma_module.ChromaVectorStore(collection_name="pdf_documents")
    store.add_documents([{"text": "hello", "embedding": [0.1] * 384}])

    assert client.deleted == ["pdf_documents"]
    assert existing_collection.added_documents == []


def test_chroma_vector_store_recreates_collection_before_adding_when_dimension_is_stale(monkeypatch) -> None:
    client = FakeClient()
    existing_collection = FakeCollection(existing_embeddings=[[0.0] * 3072])
    client.collections["pdf_documents"] = existing_collection

    monkeypatch.setattr(chroma_module.chromadb, "PersistentClient", lambda path=None: client)

    store = chroma_module.ChromaVectorStore(collection_name="pdf_documents")
    store.add_documents([{"text": "hello", "embedding": [0.1] * 384}])

    assert client.deleted == ["pdf_documents"]
    assert existing_collection.added_documents == []


def test_chroma_vector_store_handles_numpy_embeddings_from_collection(monkeypatch) -> None:
    client = FakeClient()

    class NumpyCollection(FakeCollection):
        def get(self, include=None):
            return {"embeddings": np.array([[0.0] * 3072])}

    existing_collection = NumpyCollection(existing_embeddings=[[0.0] * 3072])
    client.collections["pdf_documents"] = existing_collection

    monkeypatch.setattr(chroma_module.chromadb, "PersistentClient", lambda path=None: client)

    store = chroma_module.ChromaVectorStore(collection_name="pdf_documents")
    store.add_documents([{"text": "hello", "embedding": [0.1] * 384}])

    assert client.deleted == ["pdf_documents"]

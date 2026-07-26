from __future__ import annotations

from typing import Any, Dict, List

import chromadb


def _normalize_embedding_sequence(value: Any) -> List[List[float]]:
    if value is None:
        return []

    if isinstance(value, (list, tuple)):
        return [list(item) if isinstance(item, (list, tuple)) else [float(item)] for item in value]

    if hasattr(value, "tolist"):
        try:
            value = value.tolist()
        except Exception:
            return []

    if isinstance(value, (list, tuple)):
        return [list(item) if isinstance(item, (list, tuple)) else [float(item)] for item in value]

    return []


class ChromaVectorStore:
    """Concrete vector store implementation backed by ChromaDB."""

    def __init__(
        self,
        collection_name: str = "pdf_documents",
        persist_directory: str | None = None,
        embedding_service: Any | None = None,
    ) -> None:
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.embedding_service = embedding_service
        self.client = chromadb.PersistentClient(path=persist_directory) if persist_directory else chromadb.PersistentClient()
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def _reset_collection(self) -> None:
        try:
            self.client.delete_collection(self.collection_name)
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def _needs_collection_reset(self, embeddings: List[List[float]]) -> bool:
        if not embeddings:
            return False

        try:
            existing = self.collection.get(include=["embeddings"])
        except Exception:
            return False

        existing_embeddings = _normalize_embedding_sequence(existing.get("embeddings", []))
        if not existing_embeddings:
            return False

        current_dimension = len(existing_embeddings[0])
        incoming_dimension = len(embeddings[0])
        return current_dimension != incoming_dimension

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        if not documents:
            return

        texts = [doc.get("text", "") for doc in documents]
        embeddings = [doc.get("embedding", []) for doc in documents]
        ids = [str(index) for index in range(len(documents))]

        if self._needs_collection_reset(embeddings):
            self._reset_collection()

        try:
            self.collection.add(
                documents=texts,
                embeddings=embeddings,
                ids=ids,
            )
        except Exception as exc:
            if "dimension" in str(exc).lower():
                raise RuntimeError(
                    "The existing Chroma collection has an incompatible embedding dimension. "
                    "Please re-ingest the document so the collection is rebuilt with the current embedding model."
                ) from exc
            raise

    def similarity_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if not query.strip():
            raise ValueError("query must not be empty")

        try:
            if self.embedding_service is not None:
                query_embedding = self.embedding_service.embed([query])[0]
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                )
            else:
                results = self.collection.query(
                    query_texts=[query],
                    n_results=top_k,
                )
        except Exception as exc:
            if "dimension" in str(exc).lower():
                raise RuntimeError(
                    "The existing Chroma collection has an incompatible embedding dimension. "
                    "Please re-ingest the document so the collection is rebuilt with the current embedding model."
                ) from exc
            raise

        documents = results.get("documents", [[]])
        if not documents:
            return []

        documents = documents[0]
        embeddings = results.get("embeddings")
        if embeddings:
            embeddings = embeddings[0]
        else:
            embeddings = [None] * len(documents)

        return [
            {"text": document, "embedding": embedding}
            for document, embedding in zip(documents, embeddings)
        ]

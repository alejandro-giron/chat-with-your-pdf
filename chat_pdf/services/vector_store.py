from __future__ import annotations

from typing import Any, Dict, List, Protocol


class VectorStore(Protocol):
    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Store documents in the backing vector database."""

    def similarity_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Return the most relevant documents for the query."""


class VectorStoreService:
    """Wrap a vector store with simple validation and convenience methods."""

    def __init__(self, store: VectorStore) -> None:
        self.store = store

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        self.store.add_documents(documents)

    def similarity_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if not query.strip():
            raise ValueError("query must not be empty")

        return self.store.similarity_search(query, top_k=top_k)

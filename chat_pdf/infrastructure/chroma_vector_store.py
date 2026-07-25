from __future__ import annotations

from typing import Any, Dict, List

import chromadb


class ChromaVectorStore:
    """Concrete vector store implementation backed by ChromaDB."""

    def __init__(self, collection_name: str = "pdf_documents", persist_directory: str | None = None) -> None:
        client = chromadb.PersistentClient(path=persist_directory) if persist_directory else chromadb.PersistentClient()
        self.collection = client.get_or_create_collection(name=collection_name)

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        if not documents:
            return

        texts = [doc.get("text", "") for doc in documents]
        embeddings = [doc.get("embedding", []) for doc in documents]
        ids = [str(index) for index in range(len(documents))]

        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            ids=ids,
        )

    def similarity_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if not query.strip():
            raise ValueError("query must not be empty")

        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
        )

        documents = results.get("documents", [[]])[0]
        embeddings = results.get("embeddings", [[]])[0]

        return [
            {"text": document, "embedding": embedding}
            for document, embedding in zip(documents, embeddings)
        ]

from __future__ import annotations

from typing import Any


class IngestionService:
    """Coordinate the full document ingestion workflow."""

    def __init__(self, text_extractor, chunker, embedding_service, vector_store_service) -> None:
        self.text_extractor = text_extractor
        self.chunker = chunker
        self.embedding_service = embedding_service
        self.vector_store_service = vector_store_service

    def ingest(self, document: Any) -> None:
        text = self.text_extractor.extract_text(document)
        chunks = self.chunker.chunk(text)
        embeddings = self.embedding_service.embed(chunks)

        documents = [
            {
                "text": chunk,
                "embedding": embedding,
                "source": document.name,
            }
            for chunk, embedding in zip(chunks, embeddings)
        ]

        self.vector_store_service.add_documents(documents)

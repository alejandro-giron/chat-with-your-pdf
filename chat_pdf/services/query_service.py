from __future__ import annotations

from typing import Any, List


class QueryService:
    """Retrieve relevant document context and build a response for a user question."""

    def __init__(self, vector_store_service: Any, answer_generator: Any) -> None:
        self.vector_store_service = vector_store_service
        self.answer_generator = answer_generator

    def query(self, question: str) -> str:
        if not question.strip():
            raise ValueError("question must not be empty")

        context = self.vector_store_service.similarity_search(question, top_k=3)
        if not context:
            return "I could not find relevant information in the document."

        return self.answer_generator.answer(question, context)

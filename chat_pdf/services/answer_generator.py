from __future__ import annotations

from typing import Any, List


class AnswerGeneratorService:
    """Wrap an answer provider with basic validation and orchestration."""

    def __init__(self, provider: Any) -> None:
        self.provider = provider

    def answer(self, question: str, context: List[dict]) -> str:
        if not question.strip():
            raise ValueError("question must not be empty")

        return self.provider.answer(question, context)

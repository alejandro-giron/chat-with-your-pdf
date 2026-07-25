from __future__ import annotations

from typing import Any, List


class GeminiAnswerProvider:
    """Concrete answer provider using the Google GenAI client."""

    def __init__(self, client: Any, model_name: str = "gemini-3.5-flash-lite") -> None:
        self.client = client
        self.model_name = model_name

    def answer(self, question: str, context: List[dict]) -> str:
        context_text = "\n".join(item.get("text", "") for item in context if item.get("text"))
        prompt = (
            f"You are a helpful assistant. Answer the user's question using the provided context.\n"
            f"Question: {question}\n"
            f"Context:\n{context_text}"
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        return response.text

from chat_pdf.infrastructure.gemini_answer_provider import GeminiAnswerProvider


class DummyResponse:
    def __init__(self, text: str) -> None:
        self.text = text


class DummyClient:
    def __init__(self) -> None:
        self.calls = []

    class Models:
        def __init__(self, parent: "DummyClient") -> None:
            self.parent = parent

        def generate_content(self, *, model: str, contents: str) -> DummyResponse:
            self.parent.calls.append((model, contents))
            return DummyResponse("answer")

    @property
    def models(self) -> "DummyClient.Models":
        return DummyClient.Models(self)


def test_gemini_answer_provider_returns_model_reply() -> None:
    client = DummyClient()
    provider = GeminiAnswerProvider(client=client, model_name="test-model")

    response = provider.answer("What is this?", [{"text": "context"}])

    assert response == "answer"
    assert client.calls[0][0] == "test-model"
    assert "What is this?" in client.calls[0][1]

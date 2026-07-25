from __future__ import annotations

from google import genai

from chat_pdf.infrastructure.chroma_vector_store import ChromaVectorStore
from chat_pdf.infrastructure.gemini_answer_provider import GeminiAnswerProvider
from chat_pdf.infrastructure.gemini_embedding_provider import GeminiEmbeddingProvider
from chat_pdf.infrastructure.pdfplumber_text_extractor import PdfPlumberTextExtractor
from chat_pdf.services.answer_generator import AnswerGeneratorService
from chat_pdf.services.chunker import TextChunker
from chat_pdf.services.console_app import ConsoleApp
from chat_pdf.services.embedding_service import EmbeddingService
from chat_pdf.services.ingestion_service import IngestionService
from chat_pdf.services.query_service import QueryService
from chat_pdf.services.vector_store import VectorStoreService


def build_app() -> ConsoleApp:
    client = genai.Client()

    text_extractor = PdfPlumberTextExtractor()
    chunker = TextChunker(chunk_size=500, overlap=50)
    embedding_provider = GeminiEmbeddingProvider(client=client)
    embedding_service = EmbeddingService(embedding_provider)
    vector_store = ChromaVectorStore(persist_directory="./data/chroma_db")
    vector_store_service = VectorStoreService(vector_store)
    answer_provider = GeminiAnswerProvider(client=client)
    answer_generator = AnswerGeneratorService(answer_provider)

    ingestion_service = IngestionService(
        text_extractor=text_extractor,
        chunker=chunker,
        embedding_service=embedding_service,
        vector_store_service=vector_store_service,
    )
    query_service = QueryService(vector_store_service=vector_store_service, answer_generator=answer_generator)

    return ConsoleApp(ingestion_service=ingestion_service, query_service=query_service)


if __name__ == "__main__":
    build_app().run()
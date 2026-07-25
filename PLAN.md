# Plan: Chat with Your PDF

## Goal
Build a simple console application that:
1. Loads a local PDF file.
2. Extracts its text.
3. Splits the content into manageable chunks.
4. Generates embeddings for each chunk.
5. Stores embeddings in a ChromaDB vector database.
6. Accepts user questions and returns AI-powered answers based on the indexed document.

## Design principles
- Follow SOLID principles:
  - Single Responsibility: each class has one clear job.
  - Open/Closed: behavior is extended through interfaces and adapters instead of editing core classes.
  - Liskov Substitution: depend on abstractions, not concrete implementations.
  - Interface Segregation: expose small, focused interfaces.
  - Dependency Inversion: high-level services depend on abstractions provided by lower-level components.
- Keep the app easy to test by separating I/O, orchestration, and external integrations.

## Proposed package structure
```text
app/
  __init__.py
  domain/
    models.py
  interfaces/
    embedding_provider.py
    vector_store.py
    text_extractor.py
    chunker.py
    answer_generator.py
  services/
    pdf_loader.py
    chunking_service.py
    embedding_service.py
    vector_store_service.py
    ingestion_service.py
    query_service.py
    console_app.py
  infrastructure/
    gemini_embedding_provider.py
    chroma_vector_store.py
    pdfplumber_text_extractor.py
    llm_answer_generator.py
  tests/
    test_pdf_loader.py
    test_chunking_service.py
    test_embedding_service.py
    test_vector_store_service.py
    test_ingestion_service.py
    test_query_service.py
    test_console_app.py
```

## Core classes and responsibilities

### 1. PdfDocument
Responsibility: represent the local PDF file and expose metadata such as path and file name.
- Stores the file path.
- Validates that the file exists.
- Can be expanded later to include document metadata.

Tests:
- Creates a valid document from a real file path.
- Raises an error for a missing file.

### 2. TextExtractor
Responsibility: extract plain text from a PDF.
- Interface: `extract_text(pdf_document)`
- Concrete implementation: `PdfPlumberTextExtractor`

Tests:
- Extracts text from a known sample PDF.
- Returns an empty result for a blank page.
- Propagates extraction errors.

### 3. Chunker
Responsibility: split extracted text into smaller chunks.
- Interface: `chunk(text, chunk_size, overlap)`
- Concrete implementation: `SentenceChunker` or `FixedSizeChunker`

Tests:
- Produces the expected number of chunks.
- Preserves overlap correctly.
- Handles short text without breaking.

### 4. EmbeddingProvider
Responsibility: generate vector embeddings for chunks.
- Interface: `embed(texts)`
- Concrete implementation: `GeminiEmbeddingProvider`

Tests:
- Returns vectors with the expected dimension.
- Handles a list of input texts.
- Raises a clear error on API failures.

### 5. VectorStore
Responsibility: persist and query embeddings.
- Interface: `add_documents(documents)` and `similarity_search(query, top_k)`
- Concrete implementation: `ChromaVectorStore`

Tests:
- Adds documents successfully.
- Retrieves the most relevant results for a known query.
- Removes or updates documents correctly if needed.

### 6. DocumentIngestionService
Responsibility: orchestrate the PDF ingestion flow.
- Receives a PDF path.
- Extracts text.
- Splits into chunks.
- Generates embeddings.
- Stores results in the vector database.

Tests:
- Runs the full ingestion pipeline for a sample PDF.
- Stores one record per chunk.
- Handles failures in one step without corrupting the process.

### 7. QueryService
Responsibility: take a user question, retrieve relevant chunks, and build an answer.
- Uses the vector store to find relevant chunks.
- Sends the question and retrieved context to an AI model.
- Returns a user-friendly response.

Tests:
- Returns a response when relevant context is found.
- Returns a fallback message when no relevant chunks are found.
- Uses retrieved context in the prompt correctly.

### 8. ConsoleApp
Responsibility: provide the interactive CLI experience.
- Prompts the user for a PDF path and questions.
- Delegates to the ingestion and query services.
- Prints results to the console.

Tests:
- Starts the app with a valid input flow.
- Exits gracefully on Ctrl+C or empty input.
- Displays helpful messages for missing files or failed indexing.

## Suggested execution flow
1. User starts the console app.
2. App asks for the local PDF path.
3. `DocumentIngestionService` loads and indexes the document.
4. App prompts the user for questions.
5. `QueryService` searches the vector store and generates an answer.
6. The app displays the answer and waits for the next question.

## Testing strategy
Use pytest for all classes.
- Keep unit tests focused on one class at a time.
- Use fixtures for sample PDFs, chunk inputs, and mock embedding responses.
- Use fake implementations for external services where needed.

## Local ChromaDB setup
ChromaDB can run locally without a separate server for this MVP, which keeps development simple and avoids external infrastructure.

### Required dependencies
Install the following Python packages:
- `chromadb`
- `pypdf` or `pdfplumber` for PDF reading
- `google-generativeai` or `google-genai` for embeddings and LLM answers
- `pytest` and `pytest-mock` for testing

### Suggested local configuration
- Use a local persistence directory such as `./data/chroma_db`.
- Configure ChromaDB to persist data on disk so the vector store survives restarts.
- Keep the collection name explicit, for example `pdf_documents`.

### Example installation commands
```bash
pip install chromadb pdfplumber google-genai pytest pytest-mock
```

### Local runtime notes
- ChromaDB should be initialized with a local persistent client.
- The app should allow the database path to be configurable through an environment variable or config file.
- For local development, the database can live inside the repository under a `data/` folder.

## Implementation milestones
1. Create the domain model and interfaces.
2. Implement the PDF text extraction layer.
3. Implement chunking and embedding services.
4. Implement ChromaDB persistence.
5. Implement the query and answer workflow.
6. Add the console entry point and polish UX.
7. Expand tests until the full flow is covered.

## MVP scope
For the first version, the app should support:
- One PDF at a time.
- Local storage of the document.
- ChromaDB-backed indexing.
- Basic conversational querying through the console.

## Later enhancements
- Support multiple PDFs.
- Add metadata filtering.
- Improve chunking quality with semantic splitting.
- Add logging and retry policies.
- Introduce a web UI later if the console app proves successful.

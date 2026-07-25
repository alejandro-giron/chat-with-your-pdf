from chat_pdf.services.chunker import TextChunker


def test_chunker_splits_text_into_expected_chunks() -> None:
    text = "one two three four five six"

    chunker = TextChunker(chunk_size=3, overlap=1)
    chunks = chunker.chunk(text)

    assert chunks == ["one two three", "three four five", "five six"]


def test_chunker_returns_single_chunk_for_short_text() -> None:
    text = "short text"

    chunker = TextChunker(chunk_size=10, overlap=0)
    chunks = chunker.chunk(text)

    assert chunks == ["short text"]


def test_chunker_returns_single_chunk_when_chunk_size_exceeds_text_length() -> None:
    text = "small"

    chunker = TextChunker(chunk_size=20, overlap=0)
    chunks = chunker.chunk(text)

    assert chunks == ["small"]

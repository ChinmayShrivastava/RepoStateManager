def test_split_texts_with_metadata(english_text: str) -> None:
    """Test case for a list of texts with metadata."""
    chunk_size = 100
    metadata_str = "word " * 50
    tokenizer = tiktoken.get_encoding("cl100k_base")
    splitter = SentenceSplitter(
        chunk_size=chunk_size, chunk_overlap=0, tokenizer=tokenizer.encode
    )

    chunks = splitter.split_texts([english_text, english_text])
    assert len(chunks) == 4

    chunks = splitter.split_texts_metadata_aware(
        [english_text, english_text], [metadata_str, metadata_str]
    )
    assert len(chunks) == 8

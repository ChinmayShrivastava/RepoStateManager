def test_contiguous_text(contiguous_text: str) -> None:
    splitter = SentenceSplitter(chunk_size=100, chunk_overlap=0)
    chunks = splitter.split_text(contiguous_text)
    assert len(chunks) == 10

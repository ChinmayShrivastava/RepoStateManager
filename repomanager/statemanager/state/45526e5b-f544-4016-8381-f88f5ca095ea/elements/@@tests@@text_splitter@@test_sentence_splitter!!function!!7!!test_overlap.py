def test_overlap() -> None:
    splitter = SentenceSplitter(chunk_size=15, chunk_overlap=10)
    chunks = splitter.split_text("Hello! How are you? I am fine. And you?")
    assert len(chunks) == 1

    chunks2 = splitter.split_text(
        "Hello! How are you? I am fine. And you? This is a slightly longer sentence."
    )
    assert len(chunks2) == 3
    assert chunks2[2] == "I am fine. And you? This is a slightly longer sentence."

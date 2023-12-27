def test_split_texts_singleton() -> None:
    """Test case for a singleton list of texts."""
    sentence_text_splitter = SentenceSplitter(chunk_size=20, chunk_overlap=0)

    text = " ".join(["foo"] * 15) + "\n\n\n" + " ".join(["bar"] * 15)
    texts = [text]
    sentence_split = sentence_text_splitter.split_texts(texts)
    assert sentence_split[0] == " ".join(["foo"] * 15)
    assert sentence_split[1] == " ".join(["bar"] * 15)

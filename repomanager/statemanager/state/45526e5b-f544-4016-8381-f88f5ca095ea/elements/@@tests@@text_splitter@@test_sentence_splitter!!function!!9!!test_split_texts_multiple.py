def test_split_texts_multiple() -> None:
    """Test case for a list of texts."""
    sentence_text_splitter = SentenceSplitter(chunk_size=20, chunk_overlap=0)

    text1 = " ".join(["foo"] * 15) + "\n\n\n" + " ".join(["bar"] * 15)
    text2 = " ".join(["bar"] * 15) + "\n\n\n" + " ".join(["foo"] * 15)
    texts = [text1, text2]
    sentence_split = sentence_text_splitter.split_texts(texts)
    print(sentence_split)
    assert sentence_split[0] == " ".join(["foo"] * 15)
    assert sentence_split[1] == " ".join(["bar"] * 15)
    assert sentence_split[2] == " ".join(["bar"] * 15)
    assert sentence_split[3] == " ".join(["foo"] * 15)

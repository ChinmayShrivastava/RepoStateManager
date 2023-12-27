def test_split_long_token() -> None:
    """Test split a really long token."""
    token = "a" * 100
    tokenizer = tiktoken.get_encoding("gpt2")
    text_splitter = TokenTextSplitter(
        chunk_size=20, chunk_overlap=0, tokenizer=tokenizer.encode
    )
    chunks = text_splitter.split_text(token)
    # each text chunk may have spaces, since we join splits by separator
    assert "".join(chunks).replace(" ", "") == token

    token = ("a" * 49) + "\n" + ("a" * 50)
    text_splitter = TokenTextSplitter(
        chunk_size=20, chunk_overlap=0, tokenizer=tokenizer.encode
    )
    chunks = text_splitter.split_text(token)
    assert len(chunks[0]) == 49
    assert len(chunks[1]) == 50

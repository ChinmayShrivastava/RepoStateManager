def test_tokenizer() -> None:
    """Make sure tokenizer works.

    NOTE: we use a different tokenizer for python >= 3.9.

    """
    text = "hello world foo bar"
    tokenizer = get_tokenizer()
    assert len(tokenizer(text)) == 4

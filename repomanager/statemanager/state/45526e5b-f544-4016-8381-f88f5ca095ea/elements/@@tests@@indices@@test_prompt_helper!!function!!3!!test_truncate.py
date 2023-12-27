def test_truncate() -> None:
    """Test truncate."""
    # test prompt uses up one token
    test_prompt_txt = "test{text}"
    test_prompt = PromptTemplate(test_prompt_txt)
    # set context_window=19
    # For each text chunk, there's 4 tokens for text + 5 for the padding
    prompt_helper = PromptHelper(
        context_window=19, num_output=0, chunk_overlap_ratio=0, tokenizer=mock_tokenizer
    )
    text_chunks = ["This is a test foo bar", "Hello world bar foo"]

    truncated_chunks = prompt_helper.truncate(
        prompt=test_prompt, text_chunks=text_chunks
    )
    assert truncated_chunks == [
        "This is a test",
        "Hello world bar foo",
    ]

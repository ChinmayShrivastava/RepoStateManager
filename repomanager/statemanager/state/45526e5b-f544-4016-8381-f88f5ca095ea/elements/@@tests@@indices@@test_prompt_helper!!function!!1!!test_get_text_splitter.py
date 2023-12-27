def test_get_text_splitter() -> None:
    """Test get text splitter."""
    test_prompt_text = "This is the prompt{text}"
    test_prompt = PromptTemplate(test_prompt_text)
    prompt_helper = PromptHelper(
        context_window=11, num_output=1, chunk_overlap_ratio=0, tokenizer=mock_tokenizer
    )
    text_splitter = prompt_helper.get_text_splitter_given_prompt(
        test_prompt, 2, padding=1
    )
    assert text_splitter.chunk_size == 2
    test_text = "Hello world foo Hello world bar"
    text_chunks = text_splitter.split_text(test_text)
    assert text_chunks == ["Hello world", "foo Hello", "world bar"]
    truncated_text = truncate_text(test_text, text_splitter)
    assert truncated_text == "Hello world"

    # test with chunk_size_limit
    prompt_helper = PromptHelper(
        context_window=11,
        num_output=1,
        chunk_overlap_ratio=0,
        tokenizer=mock_tokenizer,
        chunk_size_limit=1,
    )
    text_splitter = prompt_helper.get_text_splitter_given_prompt(
        test_prompt, 2, padding=1
    )
    text_chunks = text_splitter.split_text(test_text)
    assert text_chunks == ["Hello", "world", "foo", "Hello", "world", "bar"]

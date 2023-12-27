def test_get_text_splitter_partial() -> None:
    """Test get text splitter with a partially formatted prompt."""
    # test without partially formatting
    test_prompt_text = "This is the {foo} prompt{text}"
    test_prompt = PromptTemplate(test_prompt_text)
    prompt_helper = PromptHelper(
        context_window=11, num_output=1, chunk_overlap_ratio=0, tokenizer=mock_tokenizer
    )
    text_splitter = prompt_helper.get_text_splitter_given_prompt(
        test_prompt, 2, padding=1
    )
    test_text = "Hello world foo Hello world bar"
    text_chunks = text_splitter.split_text(test_text)
    assert text_chunks == ["Hello world", "foo Hello", "world bar"]
    truncated_text = truncate_text(test_text, text_splitter)
    assert truncated_text == "Hello world"

    # test with partially formatting
    test_prompt = PromptTemplate(test_prompt_text)
    test_prompt = test_prompt.partial_format(foo="bar")
    prompt_helper = PromptHelper(
        context_window=12, num_output=1, chunk_overlap_ratio=0, tokenizer=mock_tokenizer
    )
    assert get_empty_prompt_txt(test_prompt) == "This is the bar prompt"
    text_splitter = prompt_helper.get_text_splitter_given_prompt(
        test_prompt, 2, padding=1
    )
    test_text = "Hello world foo Hello world bar"
    text_chunks = text_splitter.split_text(test_text)
    assert text_chunks == ["Hello world", "foo Hello", "world bar"]
    truncated_text = truncate_text(test_text, text_splitter)
    assert truncated_text == "Hello world"

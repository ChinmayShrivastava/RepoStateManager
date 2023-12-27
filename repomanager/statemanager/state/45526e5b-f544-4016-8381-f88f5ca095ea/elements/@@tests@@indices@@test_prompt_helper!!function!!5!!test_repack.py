def test_repack() -> None:
    """Test repack."""
    test_prompt_text = "This is the prompt{text}"
    test_prompt = PromptTemplate(test_prompt_text)
    prompt_helper = PromptHelper(
        context_window=13,
        num_output=1,
        chunk_overlap_ratio=0,
        tokenizer=mock_tokenizer,
        separator="\n\n",
    )
    text_chunks = ["Hello", "world", "foo", "Hello", "world", "bar"]
    compacted_chunks = prompt_helper.repack(test_prompt, text_chunks)
    assert compacted_chunks == ["Hello\n\nworld\n\nfoo", "Hello\n\nworld\n\nbar"]

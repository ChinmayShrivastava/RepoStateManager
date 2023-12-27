def test_get_numbered_text_from_nodes() -> None:
    """Test get_text_from_nodes."""
    # test prompt uses up one token
    test_prompt_txt = "test{text}"
    test_prompt = PromptTemplate(test_prompt_txt)
    # set context_window=17
    # For each text chunk, there's 3 for text, 5 for padding (including number)
    prompt_helper = PromptHelper(
        context_window=17, num_output=0, chunk_overlap_ratio=0, tokenizer=mock_tokenizer
    )
    node1 = TextNode(text="This is a test foo bar")
    node2 = TextNode(text="Hello world bar foo")

    text_splitter = prompt_helper.get_text_splitter_given_prompt(
        prompt=test_prompt,
        num_chunks=2,
    )
    response = get_numbered_text_from_nodes([node1, node2], text_splitter=text_splitter)
    assert str(response) == ("(1) This is a\n\n(2) Hello world bar")

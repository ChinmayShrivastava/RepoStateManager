def test_accumulate_response_async(
    mock_service_context: ServiceContext,
    documents: List[Document],
) -> None:
    """Test accumulate response."""
    # test response with ResponseMode.ACCUMULATE
    # NOTE: here we want to guarantee that prompts have 0 extra tokens
    mock_qa_prompt_tmpl = "{context_str}{query_str}"
    mock_qa_prompt = PromptTemplate(
        mock_qa_prompt_tmpl, prompt_type=PromptType.QUESTION_ANSWER
    )

    # max input size is 11, prompt is two tokens (the query) --> 9 tokens
    # --> padding is 1 --> 8 tokens
    prompt_helper = PromptHelper(
        context_window=11,
        num_output=0,
        chunk_overlap_ratio=0,
        tokenizer=mock_tokenizer,
        separator="\n\n",
        chunk_size_limit=4,
    )
    service_context = mock_service_context
    service_context.prompt_helper = prompt_helper
    cur_chunk_size = prompt_helper._get_available_chunk_size(
        mock_qa_prompt, 1, padding=1
    )
    # outside of compact, assert that chunk size is 4
    assert cur_chunk_size == 4

    # within compact, make sure that chunk size is 8
    query_str = "What is?"
    texts = [
        "This\nis\nbar",
        "This\nis\nfoo",
    ]
    builder = get_response_synthesizer(
        service_context=service_context,
        text_qa_template=mock_qa_prompt,
        response_mode=ResponseMode.ACCUMULATE,
        use_async=True,
    )

    response = builder.get_response(text_chunks=texts, query_str=query_str)
    expected = (
        "Response 1: What is?:This\n"
        "---------------------\n"
        "Response 2: What is?:is\n"
        "---------------------\n"
        "Response 3: What is?:bar\n"
        "---------------------\n"
        "Response 4: What is?:This\n"
        "---------------------\n"
        "Response 5: What is?:is\n"
        "---------------------\n"
        "Response 6: What is?:foo"
    )
    assert str(response) == expected

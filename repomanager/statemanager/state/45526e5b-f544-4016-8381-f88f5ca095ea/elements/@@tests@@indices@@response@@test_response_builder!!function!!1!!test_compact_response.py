def test_compact_response(mock_service_context: ServiceContext) -> None:
    """Test give response."""
    # test response with ResponseMode.COMPACT
    # NOTE: here we want to guarantee that prompts have 0 extra tokens
    mock_refine_prompt_tmpl = "{query_str}{existing_answer}{context_msg}"
    mock_refine_prompt = PromptTemplate(
        mock_refine_prompt_tmpl, prompt_type=PromptType.REFINE
    )

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
        "This\n\nis\n\na\n\nbar",
        "This\n\nis\n\na\n\ntest",
    ]
    builder = get_response_synthesizer(
        service_context=service_context,
        text_qa_template=mock_qa_prompt,
        refine_template=mock_refine_prompt,
        response_mode=ResponseMode.COMPACT,
    )

    response = builder.get_response(text_chunks=texts, query_str=query_str)
    assert str(response) == "What is?:This:is:a:bar:This:is:a:test"

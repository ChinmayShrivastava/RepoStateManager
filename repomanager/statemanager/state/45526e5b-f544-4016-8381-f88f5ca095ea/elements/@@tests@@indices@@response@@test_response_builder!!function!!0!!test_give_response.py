def test_give_response(
    mock_service_context: ServiceContext,
    documents: List[Document],
) -> None:
    """Test give response."""
    prompt_helper = PromptHelper(
        context_window=DEFAULT_CONTEXT_WINDOW, num_output=DEFAULT_NUM_OUTPUTS
    )

    service_context = mock_service_context
    service_context.prompt_helper = prompt_helper
    query_str = "What is?"

    # test single line
    builder = get_response_synthesizer(
        response_mode=ResponseMode.REFINE,
        service_context=service_context,
        text_qa_template=MOCK_TEXT_QA_PROMPT,
        refine_template=MOCK_REFINE_PROMPT,
    )
    response = builder.get_response(
        text_chunks=["This is a single line."], query_str=query_str
    )

    # test multiple lines
    response = builder.get_response(
        text_chunks=[documents[0].get_content()], query_str=query_str
    )
    expected_answer = (
        "What is?:"
        "Hello world.:"
        "This is a test.:"
        "This is another test.:"
        "This is a test v2."
    )
    assert str(response) == expected_answer

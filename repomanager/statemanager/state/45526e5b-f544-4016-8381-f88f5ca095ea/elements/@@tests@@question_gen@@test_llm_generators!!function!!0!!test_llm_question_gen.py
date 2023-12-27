def test_llm_question_gen(
    mock_service_context: ServiceContext,
) -> None:
    question_gen = LLMQuestionGenerator.from_defaults(
        service_context=mock_service_context
    )

    tools = [
        ToolMetadata(description="data source 1", name="source_1"),
        ToolMetadata(description="data source 2", name="source_2"),
    ]
    query = QueryBundle(query_str="What is A and B?")
    sub_questions = question_gen.generate(tools=tools, query=query)
    assert isinstance(sub_questions[0], SubQuestion)

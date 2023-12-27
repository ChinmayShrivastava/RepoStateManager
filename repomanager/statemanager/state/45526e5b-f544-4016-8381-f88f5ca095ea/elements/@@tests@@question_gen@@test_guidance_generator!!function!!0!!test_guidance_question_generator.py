def test_guidance_question_generator() -> None:
    question_gen = GuidanceQuestionGenerator.from_defaults(guidance_llm=MockLLM())

    tools = [
        ToolMetadata(name="test_tool_1", description="test_description_1"),
        ToolMetadata(name="test_tool_2", description="test_description_2"),
    ]
    output = question_gen.generate(tools=tools, query=QueryBundle("test query"))
    assert isinstance(output[0], SubQuestion)

def test_llm_program_with_messages_and_chat() -> None:
    """Test LLM program."""
    messages = [ChatMessage(role=MessageRole.USER, content="Test")]
    prompt = ChatPromptTemplate(message_templates=messages)
    output_parser = PydanticOutputParser(output_cls=TestModel)
    llm_program = LLMTextCompletionProgram.from_defaults(
        output_parser=output_parser,
        prompt=prompt,
        llm=MockChatLLM(),
    )
    # mock llm
    obj_output = llm_program()
    assert isinstance(obj_output, TestModel)
    assert obj_output.hello == "chat"

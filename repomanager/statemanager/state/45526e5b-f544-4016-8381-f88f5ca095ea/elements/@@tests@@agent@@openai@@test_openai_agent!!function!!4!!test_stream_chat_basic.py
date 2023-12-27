def test_stream_chat_basic(MockSyncOpenAI: MagicMock, add_tool: FunctionTool) -> None:
    mock_instance = MockSyncOpenAI.return_value
    mock_instance.chat.completions.create.side_effect = mock_chat_stream

    llm = OpenAI(model="gpt-3.5-turbo")

    agent = OpenAIAgent.from_tools(
        tools=[add_tool],
        llm=llm,
    )
    response = agent.stream_chat("What is 1 + 1?")
    assert isinstance(response, StreamingAgentChatResponse)
    # str() strips newline values
    assert str(response) == "This is a test!"

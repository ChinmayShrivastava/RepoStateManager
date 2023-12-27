def test_chat_no_functions(MockSyncOpenAI: MagicMock) -> None:
    mock_instance = MockSyncOpenAI.return_value
    mock_instance.chat.completions.create.return_value = mock_chat_completion()

    llm = OpenAI(model="gpt-3.5-turbo")

    agent = OpenAIAgent.from_tools(
        llm=llm,
    )
    response = agent.chat("What is 1 + 1?")
    assert isinstance(response, AgentChatResponse)
    assert response.response == "\n\nThis is a test!"

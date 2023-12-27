def test_chat_basic(
    add_tool: FunctionTool,
) -> None:
    mock_llm = MockChatLLM(
        responses=[
            ChatMessage(
                content=MOCK_ACTION_RESPONSE,
                role=MessageRole.ASSISTANT,
            ),
            ChatMessage(
                content=MOCK_FINAL_RESPONSE,
                role=MessageRole.ASSISTANT,
            ),
        ]
    )

    agent = ReActAgent.from_tools(
        tools=[add_tool],
        llm=mock_llm,
    )
    response = agent.chat("What is 1 + 1?")
    assert isinstance(response, AgentChatResponse)
    assert response.response == "2"

    chat_history = agent.chat_history
    assert chat_history == [
        ChatMessage(
            content="What is 1 + 1?",
            role=MessageRole.USER,
        ),
        ChatMessage(
            content="2",
            role=MessageRole.ASSISTANT,
        ),
    ]

def test_stream_chat_basic(
    add_tool: FunctionTool,
) -> None:
    mock_llm = MockStreamChatLLM(
        responses=[
            ChatMessage(
                content=MOCK_ACTION_RESPONSE,
                role=MessageRole.ASSISTANT,
            ),
            ChatMessage(
                content=MOCK_STREAM_FINAL_RESPONSE,
                role=MessageRole.ASSISTANT,
            ),
        ]
    )

    agent = ReActAgent.from_tools(
        tools=[add_tool],
        llm=mock_llm,
    )
    response = agent.stream_chat("What is 1 + 1?")
    assert isinstance(response, StreamingAgentChatResponse)

    # exhaust stream
    for delta in response.response_gen:
        continue
    expected_answer = MOCK_STREAM_FINAL_RESPONSE.split("Answer: ")[-1].strip()
    assert response.response == expected_answer

    assert agent.chat_history == [
        ChatMessage(
            content="What is 1 + 1?",
            role=MessageRole.USER,
        ),
        ChatMessage(
            content="2 is the final answer.",
            role=MessageRole.ASSISTANT,
        ),
    ]

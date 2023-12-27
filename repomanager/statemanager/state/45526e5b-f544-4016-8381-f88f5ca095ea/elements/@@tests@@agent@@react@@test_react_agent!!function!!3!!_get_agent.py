def _get_agent(tools: List[BaseTool]) -> ReActAgent:
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
    return ReActAgent.from_tools(
        tools=tools,
        llm=mock_llm,
    )

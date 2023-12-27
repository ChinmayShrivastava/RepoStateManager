def test_add_step(
    MockSyncOpenAI: MagicMock,
    add_tool: FunctionTool,
) -> None:
    """Test add step."""
    mock_instance = MockSyncOpenAI.return_value
    mock_instance.chat.completions.create.return_value = mock_chat_completion()

    llm = OpenAI(model="gpt-3.5-turbo")
    # sync
    agent = OpenAIAgent.from_tools(
        tools=[add_tool],
        llm=llm,
    )
    task = agent.create_task("What is 1 + 1?")
    # first step
    step_output = agent.run_step(task.task_id)
    # add human input (not used but should be in memory)
    step_output = agent.run_step(task.task_id, input="tmp")
    chat_history: List[ChatMessage] = task.extra_state["new_memory"].get_all()
    assert "tmp" in [m.content for m in chat_history]

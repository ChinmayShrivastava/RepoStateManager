def test_agent() -> None:
    """Test executor."""
    agent_runner = AgentRunner(agent_worker=MockAgentWorker(limit=2))

    # test create_task
    task = agent_runner.create_task("hello world")
    assert task.input == "hello world"
    assert task.task_id in agent_runner.state.task_dict

    # test run step
    step_output = agent_runner.run_step(task.task_id)
    assert task.extra_state["counter"] == 1
    assert str(step_output.output) == "counter: 1"
    assert step_output.is_last is False

    # test list task, get task
    assert len(agent_runner.list_tasks()) == 1
    assert agent_runner.get_task(task_id=task.task_id) == task

    # test run step again
    step_output = agent_runner.run_step(task.task_id)
    assert task.extra_state["counter"] == 2
    assert str(step_output.output) == "counter: 2"
    assert step_output.is_last is True
    assert len(agent_runner.state.task_dict[task.task_id].completed_steps) == 2

    # test e2e chat
    # NOTE: to use chat, output needs to be AgentChatResponse
    agent_runner = AgentRunner(agent_worker=MockAgentWorker(limit=10))
    response = agent_runner.chat("hello world")
    assert str(response) == "counter: 10"
    assert len(agent_runner.state.task_dict) == 1

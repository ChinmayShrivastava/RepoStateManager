def test_add_step(
    add_tool: FunctionTool,
) -> None:
    # sync
    agent = _get_agent([add_tool])
    task = agent.create_task("What is 1 + 1?")
    # first step
    step_output = agent.run_step(task.task_id)
    # add human input (not used but should be in memory)
    step_output = agent.run_step(task.task_id, input="tmp")
    observations = _get_observations(task)
    assert "tmp" in observations

    # stream_step
    agent = _get_agent([add_tool])
    task = agent.create_task("What is 1 + 1?")
    # first step
    step_output = agent.stream_step(task.task_id)
    # add human input (not used but should be in memory)
    step_output = agent.stream_step(task.task_id, input="tmp")
    observations = _get_observations(task)
    assert "tmp" in observations

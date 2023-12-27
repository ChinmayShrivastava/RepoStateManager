def test_dag_agent() -> None:
    """Test DAG agent executor."""
    agent_runner = ParallelAgentRunner(agent_worker=MockForkStepEngine(limit=2))

    # test create_task
    task = agent_runner.create_task("hello world")

    # test run step
    step_outputs = agent_runner.run_steps_in_queue(task_id=task.task_id)
    step_output = step_outputs[0]
    assert step_output.task_step.step_state["num"] == "0"
    assert str(step_output.output) == "0"
    assert step_output.is_last is False

    # test run step again
    step_outputs = agent_runner.run_steps_in_queue(task_id=task.task_id)
    assert step_outputs[0].task_step.step_state["num"] == "00"
    assert step_outputs[1].task_step.step_state["num"] == "01"
    # TODO: deal with having multiple `is_last` outputs in chat later.
    assert step_outputs[0].is_last is True
    assert step_outputs[1].is_last is True
    assert len(agent_runner.state.task_dict[task.task_id].completed_steps) == 3

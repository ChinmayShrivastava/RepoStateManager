class MockForkStepEngine(BaseAgentWorker):
    """Mock agent worker that adds an exponential # steps."""

    def __init__(self, limit: int = 2):
        """Initialize."""
        self.limit = limit

    def initialize_step(self, task: Task, **kwargs: Any) -> TaskStep:
        """Initialize step from task."""
        counter = 0
        return TaskStep(
            task_id=task.task_id,
            step_id=str(uuid.uuid4()),
            input=task.input,
            memory=task.memory,
            step_state={"num": "0", "counter": counter},
        )

    def run_step(self, step: TaskStep, task: Task, **kwargs: Any) -> TaskStepOutput:
        """Run step."""
        counter = step.step_state["counter"] + 1
        step.step_state["counter"] = counter
        is_done = counter >= self.limit

        cur_num = step.step_state["num"]

        if is_done:
            new_steps = []
        else:
            new_steps = [
                step.get_next_step(
                    step_id=str(uuid.uuid4()),
                    step_state={"num": cur_num + "0", "counter": counter},
                ),
                step.get_next_step(
                    step_id=str(uuid.uuid4()),
                    step_state={"num": cur_num + "1", "counter": counter},
                ),
            ]

        return TaskStepOutput(
            output=AgentChatResponse(response=cur_num),
            task_step=step,
            is_last=is_done,
            next_steps=new_steps,
        )

    async def arun_step(
        self, step: TaskStep, task: Task, **kwargs: Any
    ) -> TaskStepOutput:
        """Run step (async)."""
        return self.run_step(step=step, task=task, **kwargs)

    def stream_step(self, step: TaskStep, task: Task, **kwargs: Any) -> TaskStepOutput:
        """Run step (stream)."""
        # TODO: figure out if we need a different type for TaskStepOutput
        raise NotImplementedError

    async def astream_step(
        self, step: TaskStep, task: Task, **kwargs: Any
    ) -> TaskStepOutput:
        """Run step (async stream)."""
        raise NotImplementedError

    def finalize_task(self, task: Task, **kwargs: Any) -> None:
        """Finalize task, after all the steps are completed."""

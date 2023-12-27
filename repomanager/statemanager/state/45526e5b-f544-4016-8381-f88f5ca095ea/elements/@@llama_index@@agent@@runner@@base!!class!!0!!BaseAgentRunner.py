class BaseAgentRunner(BaseAgent):
    """Base agent runner."""

    @abstractmethod
    def create_task(self, input: str, **kwargs: Any) -> Task:
        """Create task."""

    @abstractmethod
    def delete_task(
        self,
        task_id: str,
    ) -> None:
        """Delete task.

        NOTE: this will not delete any previous executions from memory.

        """

    @abstractmethod
    def list_tasks(self, **kwargs: Any) -> List[Task]:
        """List tasks."""

    @abstractmethod
    def get_task(self, task_id: str, **kwargs: Any) -> Task:
        """Get task."""

    @abstractmethod
    def get_upcoming_steps(self, task_id: str, **kwargs: Any) -> List[TaskStep]:
        """Get upcoming steps."""

    @abstractmethod
    def get_completed_steps(self, task_id: str, **kwargs: Any) -> List[TaskStepOutput]:
        """Get completed steps."""

    def get_completed_step(
        self, task_id: str, step_id: str, **kwargs: Any
    ) -> TaskStepOutput:
        """Get completed step."""
        # call get_completed_steps, and then find the right task
        completed_steps = self.get_completed_steps(task_id, **kwargs)
        for step_output in completed_steps:
            if step_output.task_step.step_id == step_id:
                return step_output
        raise ValueError(f"Could not find step_id: {step_id}")

    @abstractmethod
    def run_step(
        self,
        task_id: str,
        input: Optional[str] = None,
        step: Optional[TaskStep] = None,
        **kwargs: Any,
    ) -> TaskStepOutput:
        """Run step."""

    @abstractmethod
    async def arun_step(
        self,
        task_id: str,
        input: Optional[str] = None,
        step: Optional[TaskStep] = None,
        **kwargs: Any,
    ) -> TaskStepOutput:
        """Run step (async)."""

    @abstractmethod
    def stream_step(
        self,
        task_id: str,
        input: Optional[str] = None,
        step: Optional[TaskStep] = None,
        **kwargs: Any,
    ) -> TaskStepOutput:
        """Run step (stream)."""

    @abstractmethod
    async def astream_step(
        self,
        task_id: str,
        input: Optional[str] = None,
        step: Optional[TaskStep] = None,
        **kwargs: Any,
    ) -> TaskStepOutput:
        """Run step (async stream)."""

    @abstractmethod
    def finalize_response(
        self,
        task_id: str,
        step_output: Optional[TaskStepOutput] = None,
    ) -> AGENT_CHAT_RESPONSE_TYPE:
        """Finalize response."""

    @abstractmethod
    def undo_step(self, task_id: str) -> None:
        """Undo previous step."""
        raise NotImplementedError("undo_step not implemented")

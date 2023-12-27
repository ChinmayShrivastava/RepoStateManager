class DAGTaskState(BaseModel):
    """DAG Task state."""

    task: Task = Field(..., description="Task.")
    root_step: TaskStep = Field(..., description="Root step.")
    step_queue: Deque[TaskStep] = Field(
        default_factory=deque, description="Task step queue."
    )
    completed_steps: List[TaskStepOutput] = Field(
        default_factory=list, description="Completed step outputs."
    )

    @property
    def task_id(self) -> str:
        """Task id."""
        return self.task.task_id

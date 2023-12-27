class TaskState(BaseModel):
    """Task state."""

    task: Task = Field(..., description="Task.")
    step_queue: Deque[TaskStep] = Field(
        default_factory=deque, description="Task step queue."
    )
    completed_steps: List[TaskStepOutput] = Field(
        default_factory=list, description="Completed step outputs."
    )

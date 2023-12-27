class TaskStepOutput(BaseModel):
    """Agent task step output."""

    output: Any = Field(..., description="Task step output")
    task_step: TaskStep = Field(..., description="Task step input")
    next_steps: List[TaskStep] = Field(..., description="Next steps to be executed.")
    is_last: bool = Field(default=False, description="Is this the last step?")

    def __str__(self) -> str:
        """String representation."""
        return str(self.output)

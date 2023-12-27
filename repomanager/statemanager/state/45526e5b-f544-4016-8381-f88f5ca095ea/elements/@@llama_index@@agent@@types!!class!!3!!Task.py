class Task(BaseModel):
    """Agent Task.

    Represents a "run" of an agent given a user input.

    """

    task_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), type=str, description="Task ID"
    )
    input: str = Field(..., type=str, description="User input")

    # NOTE: this is state that may be modified throughout the course of execution of the task
    memory: BaseMemory = Field(
        ...,
        type=BaseMemory,
        description=(
            "Conversational Memory. Maintains state before execution of this task."
        ),
    )

    extra_state: Dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Additional user-specified state for a given task. "
            "Can be modified throughout the execution of a task."
        ),
    )

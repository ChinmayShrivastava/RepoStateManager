class TaskStep(BaseModel):
    """Agent task step.

    Represents a single input step within the execution run ("Task") of an agent
    given a user input.

    The output is returned as a `TaskStepOutput`.

    """

    task_id: str = Field(..., diescription="Task ID")
    step_id: str = Field(..., description="Step ID")
    input: Optional[str] = Field(default=None, description="User input")
    # memory: BaseMemory = Field(
    #     ..., type=BaseMemory, description="Conversational Memory"
    # )
    step_state: Dict[str, Any] = Field(
        default_factory=dict, description="Additional state for a given step."
    )

    # NOTE: the state below may change throughout the course of execution
    # this tracks the relationships to other steps
    next_steps: Dict[str, "TaskStep"] = Field(
        default_factory=dict, description="Next steps to be executed."
    )
    prev_steps: Dict[str, "TaskStep"] = Field(
        default_factory=dict,
        description="Previous steps that were dependencies for this step.",
    )
    is_ready: bool = Field(
        default=True, description="Is this step ready to be executed?"
    )

    def get_next_step(
        self,
        step_id: str,
        input: Optional[str] = None,
        step_state: Optional[Dict[str, Any]] = None,
    ) -> "TaskStep":
        """Convenience function to get next step.

        Preserve task_id, memory, step_state.

        """
        return TaskStep(
            task_id=self.task_id,
            step_id=step_id,
            input=input,
            # memory=self.memory,
            step_state=step_state or self.step_state,
        )

    def link_step(
        self,
        next_step: "TaskStep",
    ) -> None:
        """Link to next step.

        Add link from this step to next, and from next step to current.

        """
        self.next_steps[next_step.step_id] = next_step
        next_step.prev_steps[self.step_id] = self

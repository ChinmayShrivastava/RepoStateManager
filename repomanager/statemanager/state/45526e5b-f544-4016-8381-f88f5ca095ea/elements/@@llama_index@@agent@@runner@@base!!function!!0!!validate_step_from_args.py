def validate_step_from_args(
    task_id: str, input: Optional[str] = None, step: Optional[Any] = None, **kwargs: Any
) -> Optional[TaskStep]:
    """Validate step from args."""
    if step is not None:
        if input is not None:
            raise ValueError("Cannot specify both `step` and `input`")
        if not isinstance(step, TaskStep):
            raise ValueError(f"step must be TaskStep: {step}")
        return step
    else:
        return (
            None
            if input is None
            else TaskStep(
                task_id=task_id, step_id=str(uuid.uuid4()), input=input, **kwargs
            )
        )

def add_user_step_to_reasoning(
    step: TaskStep,
    memory: BaseMemory,
    current_reasoning: List[BaseReasoningStep],
    verbose: bool = False,
) -> None:
    """Add user step to memory."""
    if "is_first" in step.step_state and step.step_state["is_first"]:
        # add to new memory
        memory.put(ChatMessage(content=step.input, role=MessageRole.USER))
        step.step_state["is_first"] = False
    else:
        reasoning_step = ObservationReasoningStep(observation=step.input)
        current_reasoning.append(reasoning_step)
        if verbose:
            print(f"Added user message to memory: {step.input}")

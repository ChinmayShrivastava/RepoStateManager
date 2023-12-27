def _get_default_prompt_helper(
    llm_metadata: LLMMetadata,
    context_window: Optional[int] = None,
    num_output: Optional[int] = None,
) -> PromptHelper:
    """Get default prompt helper."""
    if context_window is not None:
        llm_metadata.context_window = context_window
    if num_output is not None:
        llm_metadata.num_output = num_output
    return PromptHelper.from_llm_metadata(llm_metadata=llm_metadata)

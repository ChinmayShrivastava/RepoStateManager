def get_callable(llm: Optional["BaseLLM"]) -> Optional[Callable]:
    """Get callable."""
    if llm is None:
        return None

    return llm.__call__

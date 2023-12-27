def watsonx_model_to_context_size(model_id: str) -> Union[int, None]:
    """Calculate the maximum number of tokens possible to generate for a model.

    Args:
        model_id: The model name we want to know the context size for.

    Returns:
        The maximum context size
    """
    token_limit = WATSONX_MODELS.get(model_id, None)

    if token_limit is None:
        raise ValueError(f"Model name {model_id} not found in {WATSONX_MODELS.keys()}")

    return token_limit

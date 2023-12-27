def openai_modelname_to_contextsize(modelname: str) -> int:
    import litellm

    """Calculate the maximum number of tokens possible to generate for a model.

    Args:
        modelname: The modelname we want to know the context size for.

    Returns:
        The maximum context size

    Example:
        .. code-block:: python

            max_tokens = openai.modelname_to_contextsize("text-davinci-003")

    Modified from:
        https://github.com/hwchase17/langchain/blob/master/langchain/llms/openai.py
    """
    # handling finetuned models
    if modelname.startswith("ft:"):
        modelname = modelname.split(":")[1]
    elif ":ft-" in modelname:  # legacy fine-tuning
        modelname = modelname.split(":")[0]

    try:
        context_size = int(litellm.get_max_tokens(modelname))
    except Exception:
        context_size = 2048  # by default assume models have at least 2048 tokens

    if context_size is None:
        raise ValueError(
            f"Unknown model: {modelname}. Please provide a valid OpenAI model name."
            "Known models are: "
            + ", ".join(litellm.model_list)
            + "\nKnown providers are: "
            + ", ".join(litellm.provider_list)
        )

    return context_size

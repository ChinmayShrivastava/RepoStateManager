def modelname_to_contextsize(modelname: str) -> int:
    """Calculate the maximum number of tokens possible to generate for a model.

    Args:
        modelname: The modelname we want to know the context size for.

    Returns:
        The maximum context size

    Example:
        .. code-block:: python

            max_tokens = modelname_to_contextsize("text-davinci-003")
    """
    # handling finetuned models
    if "ft-" in modelname:  # legacy fine-tuning
        modelname = modelname.split(":")[0]
    elif modelname.startswith("ft:"):
        modelname = modelname.split(":")[1]

    if modelname in DISCONTINUED_MODELS:
        raise ValueError(
            f"Model {modelname} has been discontinued. " "Please choose another model."
        )

    context_size = ALL_AVAILABLE_MODELS.get(modelname, None)

    if context_size is None:
        raise ValueError(
            f"Unknown model: {modelname}. Please provide a valid model name."
            "Known models are: " + ", ".join(ALL_AVAILABLE_MODELS.keys())
        )

    return context_size

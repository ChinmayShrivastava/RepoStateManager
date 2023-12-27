def cohere_modelname_to_contextsize(modelname: str) -> int:
    context_size = ALL_AVAILABLE_MODELS.get(modelname, None)
    if context_size is None:
        raise ValueError(
            f"Unknown model: {modelname}. Please provide a valid Cohere model name."
            "Known models are: " + ", ".join(ALL_AVAILABLE_MODELS.keys())
        )

    return context_size

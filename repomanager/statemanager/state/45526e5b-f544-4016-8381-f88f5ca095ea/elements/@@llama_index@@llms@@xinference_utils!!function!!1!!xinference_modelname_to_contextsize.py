def xinference_modelname_to_contextsize(modelname: str) -> int:
    context_size = XINFERENCE_MODEL_SIZES.get(modelname, None)

    if context_size is None:
        raise ValueError(
            f"Unknown model: {modelname}. Please provide a valid OpenAI model name."
            "Known models are: " + ", ".join(XINFERENCE_MODEL_SIZES.keys())
        )

    return context_size

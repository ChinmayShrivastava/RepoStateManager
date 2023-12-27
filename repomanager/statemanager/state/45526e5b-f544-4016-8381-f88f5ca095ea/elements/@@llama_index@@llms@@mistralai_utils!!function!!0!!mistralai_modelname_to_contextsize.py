def mistralai_modelname_to_contextsize(modelname: str) -> int:
    if modelname not in MISTRALAI_MODELS:
        raise ValueError(
            f"Unknown model: {modelname}. Please provide a valid MistralAI model name."
            "Known models are: " + ", ".join(MISTRALAI_MODELS.keys())
        )

    return MISTRALAI_MODELS[modelname]

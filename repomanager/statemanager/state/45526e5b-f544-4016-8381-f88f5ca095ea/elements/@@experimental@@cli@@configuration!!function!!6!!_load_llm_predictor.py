def _load_llm_predictor(config: ConfigParser) -> LLMPredictor:
    """Internal function to load LLM predictor based on configuration."""
    model_type = config["llm_predictor"]["type"].lower()
    if model_type == "default":
        llm = _load_llm(config["llm_predictor"])
        return LLMPredictor(llm=llm)
    elif model_type == "structured":
        llm = _load_llm(config["llm_predictor"])
        return StructuredLLMPredictor(llm=llm)
    else:
        raise KeyError("llm_predictor.type")

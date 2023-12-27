def get_engine(
    mode: str,
    model: str,
    mode_model_dict: Dict[Tuple[OpenAIEmbeddingMode, str], OpenAIEmbeddingModeModel],
) -> OpenAIEmbeddingModeModel:
    """Get engine."""
    key = (OpenAIEmbeddingMode(mode), OpenAIEmbeddingModelType(model))
    if key not in mode_model_dict:
        raise ValueError(f"Invalid mode, model combination: {key}")
    return mode_model_dict[key]

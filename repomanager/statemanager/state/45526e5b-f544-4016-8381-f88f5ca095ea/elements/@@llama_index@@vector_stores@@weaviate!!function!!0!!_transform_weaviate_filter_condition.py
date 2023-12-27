def _transform_weaviate_filter_condition(condition: str) -> str:
    """Translate standard metadata filter op to Chroma specific spec."""
    if condition == "and":
        return "And"
    elif condition == "or":
        return "Or"
    else:
        raise ValueError(f"Filter condition {condition} not supported")

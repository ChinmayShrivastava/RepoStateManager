def _transform_chroma_filter_condition(condition: str) -> str:
    """Translate standard metadata filter op to Chroma specific spec."""
    if condition == "and":
        return "$and"
    elif condition == "or":
        return "$or"
    else:
        raise ValueError(f"Filter condition {condition} not supported")

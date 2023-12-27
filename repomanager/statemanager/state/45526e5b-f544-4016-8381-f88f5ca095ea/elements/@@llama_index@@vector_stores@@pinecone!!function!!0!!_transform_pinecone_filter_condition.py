def _transform_pinecone_filter_condition(condition: str) -> str:
    """Translate standard metadata filter op to Pinecone specific spec."""
    if condition == "and":
        return "$and"
    elif condition == "or":
        return "$or"
    else:
        raise ValueError(f"Filter condition {condition} not supported")

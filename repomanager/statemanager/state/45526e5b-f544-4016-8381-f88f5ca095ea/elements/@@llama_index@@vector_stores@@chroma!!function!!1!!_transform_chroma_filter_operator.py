def _transform_chroma_filter_operator(operator: str) -> str:
    """Translate standard metadata filter operator to Chroma specific spec."""
    if operator == "!=":
        return "$ne"
    elif operator == "==":
        return "$eq"
    elif operator == ">":
        return "$gt"
    elif operator == "<":
        return "$lt"
    elif operator == ">=":
        return "$gte"
    elif operator == "<=":
        return "$lte"
    else:
        raise ValueError(f"Filter operator {operator} not supported")

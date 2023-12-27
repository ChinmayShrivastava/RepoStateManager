def _transform_pinecone_filter_operator(operator: str) -> str:
    """Translate standard metadata filter operator to Pinecone specific spec."""
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
    elif operator == "in":
        return "$in"
    elif operator == "nin":
        return "$nin"
    else:
        raise ValueError(f"Filter operator {operator} not supported")

def _transform_weaviate_filter_operator(operator: str) -> str:
    """Translate standard metadata filter operator to Chroma specific spec."""
    if operator == "!=":
        return "NotEqual"
    elif operator == "==":
        return "Equal"
    elif operator == ">":
        return "GreaterThan"
    elif operator == "<":
        return "LessThan"
    elif operator == ">=":
        return "GreaterThanEqual"
    elif operator == "<=":
        return "LessThanEqual"
    else:
        raise ValueError(f"Filter operator {operator} not supported")

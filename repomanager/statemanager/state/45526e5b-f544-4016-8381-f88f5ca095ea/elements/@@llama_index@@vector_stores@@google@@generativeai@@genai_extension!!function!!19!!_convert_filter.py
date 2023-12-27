def _convert_filter(fs: Optional[Dict[str, Any]]) -> List[genai.MetadataFilter]:
    if fs is None:
        return []
    assert isinstance(fs, dict)

    filters: List[genai.MetadataFilter] = []
    for key, value in fs.items():
        if isinstance(value, str):
            condition = genai.Condition(
                operation=genai.Condition.Operator.EQUAL, string_value=value
            )
        elif isinstance(value, (float, int)):
            condition = genai.Condition(
                operation=genai.Condition.Operator.EQUAL, numeric_value=value
            )
        else:
            raise ValueError(f"Filter value {value} is not supported")

        filters.append(genai.MetadataFilter(key=key, conditions=[condition]))

    return filters

def _convert_to_metadata(metadata: Dict[str, Any]) -> List[genai.CustomMetadata]:
    cs: List[genai.CustomMetadata] = []
    for key, value in metadata.items():
        if isinstance(value, str):
            c = genai.CustomMetadata(key=key, string_value=value)
        elif isinstance(value, (float, int)):
            c = genai.CustomMetadata(key=key, numeric_value=value)
        else:
            raise ValueError(f"Metadata value {value} is not supported")

        cs.append(c)
    return cs

def __get_painless_scripting_source(
    space_type: str, vector_field: str = "embedding"
) -> str:
    """For Painless Scripting, it returns the script source based on space type."""
    source_value = f"(1.0 + {space_type}(params.query_value, doc['{vector_field}']))"
    if space_type == "cosineSimilarity":
        return source_value
    else:
        return f"1/{source_value}"

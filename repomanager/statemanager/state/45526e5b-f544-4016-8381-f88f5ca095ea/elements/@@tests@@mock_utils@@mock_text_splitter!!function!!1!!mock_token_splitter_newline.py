def mock_token_splitter_newline(
    text: str, metadata_str: Optional[str] = None
) -> List[str]:
    """Mock token splitter by newline."""
    if text == "":
        return []
    return text.split("\n")

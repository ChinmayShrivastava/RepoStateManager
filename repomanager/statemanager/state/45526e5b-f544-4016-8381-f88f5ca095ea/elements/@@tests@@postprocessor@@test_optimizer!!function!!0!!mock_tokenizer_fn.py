def mock_tokenizer_fn(text: str) -> List[str]:
    """Mock tokenizer function."""
    # split by words
    return text.split(" ")

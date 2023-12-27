def mock_tokenizer_fn2(text: str) -> List[str]:
    """Mock tokenizer function."""
    # split by words
    return text.split(",")

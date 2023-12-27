def mock_get_text_embedding(text: str) -> List[float]:
    """Mock get text embedding."""
    # assume dimensions are 5
    if text == "hello":
        return [1, 0, 0, 0, 0]
    elif text == "world":
        return [0, 1, 0, 0, 0]
    elif text == "foo":
        return [0, 0, 1, 0, 0]
    elif text == "bar":
        return [0, 0, 0, 1, 0]
    elif text == "abc":
        return [0, 0, 0, 0, 1]
    else:
        raise ValueError("Invalid text for `mock_get_text_embedding`.")

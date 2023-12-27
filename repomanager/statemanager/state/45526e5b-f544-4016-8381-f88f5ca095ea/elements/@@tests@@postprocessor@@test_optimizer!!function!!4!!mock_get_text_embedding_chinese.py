def mock_get_text_embedding_chinese(text: str) -> List[float]:
    """Mock get text embedding."""
    # assume dimensions are 5
    if text == "你":
        return [1, 0, 0, 0, 0]
    elif text == "好":
        return [0, 1, 0, 0, 0]
    elif text == "世":
        return [0, 0, 1, 0, 0]
    elif text == "界":
        return [0, 0, 0, 1, 0]
    elif text == "abc":
        return [0, 0, 0, 0, 1]
    else:
        raise ValueError("Invalid text for `mock_get_text_embedding_chinese`.", text)

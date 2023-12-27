def test_get_colored_text() -> None:
    """Test _get_colored_text function."""
    text = "Hello, world!"
    for color in _LLAMA_INDEX_COLORS:
        colored_text = _get_colored_text(text, color)
        assert colored_text.startswith("\033[1;3;")
        assert colored_text.endswith("m" + text + "\033[0m")

    for color in _ANSI_COLORS:
        colored_text = _get_colored_text(text, color)
        assert colored_text.startswith("\033[1;3;")
        assert colored_text.endswith("m" + text + "\033[0m")

    # Test with an unsupported color
    colored_text = _get_colored_text(text, "unsupported_color")
    assert colored_text == f"\033[1;3m{text}\033[0m"  # just bolded and italicized

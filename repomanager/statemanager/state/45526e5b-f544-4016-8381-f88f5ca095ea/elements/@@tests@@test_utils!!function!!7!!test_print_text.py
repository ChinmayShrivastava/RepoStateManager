def test_print_text(capsys: CaptureFixture) -> None:
    """Test print_text function."""
    text = "Hello, world!"
    for color in _LLAMA_INDEX_COLORS:
        print_text(text, color)
        captured = capsys.readouterr()
        assert captured.out == f"\033[1;3;{_LLAMA_INDEX_COLORS[color]}m{text}\033[0m"

    for color in _ANSI_COLORS:
        print_text(text, color)
        captured = capsys.readouterr()
        assert captured.out == f"\033[1;3;{_ANSI_COLORS[color]}m{text}\033[0m"

    # Test with an unsupported color
    print_text(text, "unsupported_color")
    captured = capsys.readouterr()
    assert captured.out == f"\033[1;3m{text}\033[0m"

    # Test without color
    print_text(text)
    captured = capsys.readouterr()
    assert captured.out == f"{text}"

    # Test with end
    print_text(text, end=" ")
    captured = capsys.readouterr()
    assert captured.out == f"{text} "

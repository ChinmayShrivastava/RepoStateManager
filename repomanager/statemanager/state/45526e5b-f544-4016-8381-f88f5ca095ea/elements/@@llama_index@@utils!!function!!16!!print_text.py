def print_text(text: str, color: Optional[str] = None, end: str = "") -> None:
    """
    Print the text with the specified color.

    Args:
        text (str): Text to be printed.
        color (str, optional): Color to be applied to the text. Supported colors are:
            llama_pink, llama_blue, llama_turquoise, llama_lavender,
            red, green, yellow, blue, magenta, cyan, pink.
        end (str, optional): String appended after the last character of the text.

    Returns:
        None
    """
    text_to_print = _get_colored_text(text, color) if color is not None else text
    print(text_to_print, end=end)

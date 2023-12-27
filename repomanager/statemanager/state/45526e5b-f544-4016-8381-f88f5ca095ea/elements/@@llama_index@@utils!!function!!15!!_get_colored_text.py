def _get_colored_text(text: str, color: str) -> str:
    """
    Get the colored version of the input text.

    Args:
        text (str): Input text.
        color (str): Color to be applied to the text.

    Returns:
        str: Colored version of the input text.
    """
    all_colors = {**_LLAMA_INDEX_COLORS, **_ANSI_COLORS}

    if color not in all_colors:
        return f"\033[1;3m{text}\033[0m"  # just bolded and italicized

    color = all_colors[color]

    return f"\033[1;3;{color}m{text}\033[0m"

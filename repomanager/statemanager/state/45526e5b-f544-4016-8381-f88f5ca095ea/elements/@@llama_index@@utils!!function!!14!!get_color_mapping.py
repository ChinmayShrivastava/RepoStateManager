def get_color_mapping(
    items: List[str], use_llama_index_colors: bool = True
) -> Dict[str, str]:
    """
    Get a mapping of items to colors.

    Args:
        items (List[str]): List of items to be mapped to colors.
        use_llama_index_colors (bool, optional): Flag to indicate
        whether to use LlamaIndex colors or ANSI colors.
            Defaults to True.

    Returns:
        Dict[str, str]: Mapping of items to colors.
    """
    if use_llama_index_colors:
        color_palette = _LLAMA_INDEX_COLORS
    else:
        color_palette = _ANSI_COLORS

    colors = list(color_palette.keys())
    return {item: colors[i % len(colors)] for i, item in enumerate(items)}

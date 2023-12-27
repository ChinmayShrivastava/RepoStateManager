def test_get_color_mapping() -> None:
    """Test get_color_mapping function."""
    items = ["item1", "item2", "item3", "item4"]
    color_mapping = get_color_mapping(items)
    assert len(color_mapping) == len(items)
    assert set(color_mapping.keys()) == set(items)
    assert all(color in _LLAMA_INDEX_COLORS for color in color_mapping.values())

    color_mapping_ansi = get_color_mapping(items, use_llama_index_colors=False)
    assert len(color_mapping_ansi) == len(items)
    assert set(color_mapping_ansi.keys()) == set(items)
    assert all(color in _ANSI_COLORS for color in color_mapping_ansi.values())

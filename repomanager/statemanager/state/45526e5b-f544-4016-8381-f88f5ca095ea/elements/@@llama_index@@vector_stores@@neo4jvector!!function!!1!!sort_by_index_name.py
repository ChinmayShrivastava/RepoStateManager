def sort_by_index_name(
    lst: List[Dict[str, Any]], index_name: str
) -> List[Dict[str, Any]]:
    """Sort first element to match the index_name if exists."""
    return sorted(lst, key=lambda x: x.get("index_name") != index_name)

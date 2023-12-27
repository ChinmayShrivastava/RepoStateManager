def get_sorted_node_list(node_dict: Dict[int, BaseNode]) -> List[BaseNode]:
    """Get sorted node list. Used by tree-strutured indices."""
    sorted_indices = sorted(node_dict.keys())
    return [node_dict[index] for index in sorted_indices]

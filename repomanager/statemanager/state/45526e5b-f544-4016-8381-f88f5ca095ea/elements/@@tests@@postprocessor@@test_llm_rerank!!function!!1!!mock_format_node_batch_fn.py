def mock_format_node_batch_fn(nodes: List[BaseNode]) -> str:
    """Mock format node batch fn."""
    return "\n".join([node.get_content() for node in nodes])

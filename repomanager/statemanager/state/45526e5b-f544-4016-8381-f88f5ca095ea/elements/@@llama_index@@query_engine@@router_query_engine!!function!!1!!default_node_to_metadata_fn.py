def default_node_to_metadata_fn(node: BaseNode) -> ToolMetadata:
    """Default node to metadata function.

    We use the node's text as the Tool description.

    """
    metadata = node.metadata or {}
    if "tool_name" not in metadata:
        raise ValueError("Node must have a tool_name in metadata.")
    return ToolMetadata(name=metadata["tool_name"], description=node.get_content())

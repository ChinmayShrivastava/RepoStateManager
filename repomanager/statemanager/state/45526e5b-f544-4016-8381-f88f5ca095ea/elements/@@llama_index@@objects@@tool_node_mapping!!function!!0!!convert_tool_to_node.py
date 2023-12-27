def convert_tool_to_node(tool: BaseTool) -> TextNode:
    """Function convert Tool to node."""
    node_text = (
        f"Tool name: {tool.metadata.name}\n"
        f"Tool description: {tool.metadata.description}\n"
    )
    if tool.metadata.fn_schema is not None:
        node_text += f"Tool schema: {tool.metadata.fn_schema.schema()}\n"
    return TextNode(
        text=node_text,
        metadata={"name": tool.metadata.name},
        excluded_embed_metadata_keys=["name"],
        excluded_llm_metadata_keys=["name"],
    )

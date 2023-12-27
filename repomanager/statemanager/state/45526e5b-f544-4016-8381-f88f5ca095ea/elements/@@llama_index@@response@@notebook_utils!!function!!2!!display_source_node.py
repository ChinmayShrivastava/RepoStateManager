def display_source_node(
    source_node: NodeWithScore,
    source_length: int = 100,
    show_source_metadata: bool = False,
    metadata_mode: MetadataMode = MetadataMode.NONE,
) -> None:
    """Display source node for jupyter notebook."""
    source_text_fmt = truncate_text(
        source_node.node.get_content(metadata_mode=metadata_mode).strip(), source_length
    )
    text_md = (
        f"**Node ID:** {source_node.node.node_id}<br>"
        f"**Similarity:** {source_node.score}<br>"
        f"**Text:** {source_text_fmt}<br>"
    )
    if show_source_metadata:
        text_md += f"**Metadata:** {source_node.node.metadata}<br>"
    if isinstance(source_node.node, ImageNode):
        text_md += "**Image:**"

    display(Markdown(text_md))
    if isinstance(source_node.node, ImageNode) and source_node.node.image is not None:
        display_image(source_node.node.image)

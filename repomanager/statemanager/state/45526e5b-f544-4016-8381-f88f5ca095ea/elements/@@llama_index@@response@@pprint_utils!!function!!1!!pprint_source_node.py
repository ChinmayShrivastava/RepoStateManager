def pprint_source_node(
    source_node: NodeWithScore, source_length: int = 350, wrap_width: int = 70
) -> None:
    """Display source node for jupyter notebook."""
    source_text_fmt = truncate_text(
        source_node.node.get_content().strip(), source_length
    )
    print(f"Node ID: {source_node.node.node_id}")
    print(f"Similarity: {source_node.score}")
    print(textwrap.fill(f"Text: {source_text_fmt}\n", width=wrap_width))

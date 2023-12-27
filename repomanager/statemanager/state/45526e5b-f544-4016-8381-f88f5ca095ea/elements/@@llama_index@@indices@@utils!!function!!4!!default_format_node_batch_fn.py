def default_format_node_batch_fn(
    summary_nodes: List[BaseNode],
) -> str:
    """Default format node batch function.

    Assign each summary node a number, and format the batch of nodes.

    """
    fmt_node_txts = []
    for idx in range(len(summary_nodes)):
        number = idx + 1
        fmt_node_txts.append(
            f"Document {number}:\n"
            f"{summary_nodes[idx].get_content(metadata_mode=MetadataMode.LLM)}"
        )
    return "\n\n".join(fmt_node_txts)

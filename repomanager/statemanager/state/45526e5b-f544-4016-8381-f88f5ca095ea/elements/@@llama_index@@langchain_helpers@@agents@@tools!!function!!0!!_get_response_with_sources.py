def _get_response_with_sources(response: RESPONSE_TYPE) -> str:
    """Return a response with source node info."""
    source_data: List[Dict[str, Any]] = []
    for source_node in response.source_nodes:
        metadata = {}
        if isinstance(source_node.node, TextNode):
            start = source_node.node.start_char_idx
            end = source_node.node.end_char_idx
            if start is not None and end is not None:
                metadata.update({"start_char_idx": start, "end_char_idx": end})

        source_data.append(metadata)
        source_data[-1]["ref_doc_id"] = source_node.node.ref_doc_id
        source_data[-1]["score"] = source_node.score
    return str({"answer": str(response), "sources": source_data})

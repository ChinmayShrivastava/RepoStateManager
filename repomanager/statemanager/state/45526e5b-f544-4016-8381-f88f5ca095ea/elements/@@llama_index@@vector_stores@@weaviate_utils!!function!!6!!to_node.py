def to_node(entry: Dict, text_key: str = DEFAULT_TEXT_KEY) -> TextNode:
    """Convert to Node."""
    additional = entry.pop("_additional")
    text = entry.pop(text_key, "")
    embedding = additional.pop("vector", None)
    try:
        node = metadata_dict_to_node(entry)
        node.text = text
        node.embedding = embedding
    except Exception as e:
        _logger.debug("Failed to parse Node metadata, fallback to legacy logic.", e)
        metadata, node_info, relationships = legacy_metadata_dict_to_node(entry)

        node = TextNode(
            text=text,
            id_=additional["id"],
            metadata=metadata,
            start_char_idx=node_info.get("start", None),
            end_char_idx=node_info.get("end", None),
            relationships=relationships,
            embedding=embedding,
        )
    return node

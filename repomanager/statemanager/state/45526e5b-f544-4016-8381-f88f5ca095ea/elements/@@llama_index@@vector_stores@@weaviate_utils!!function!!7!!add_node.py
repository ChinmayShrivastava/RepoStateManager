def add_node(
    client: "Client",
    node: BaseNode,
    class_name: str,
    batch: Optional[Any] = None,
    text_key: str = DEFAULT_TEXT_KEY,
) -> None:
    """Add node."""
    metadata = {}
    metadata[text_key] = node.get_content(metadata_mode=MetadataMode.NONE) or ""

    additional_metadata = node_to_metadata_dict(
        node, remove_text=True, flat_metadata=False
    )
    metadata.update(additional_metadata)

    vector = node.get_embedding()
    id = node.node_id

    # if batch object is provided (via a context manager), use that instead
    if batch is not None:
        batch.add_data_object(metadata, class_name, id, vector)
    else:
        client.batch.add_data_object(metadata, class_name, id, vector)

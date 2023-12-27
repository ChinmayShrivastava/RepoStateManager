def embed_image_nodes(
    nodes: Sequence[ImageNode],
    embed_model: MultiModalEmbedding,
    show_progress: bool = False,
) -> Dict[str, List[float]]:
    """Get image embeddings of the given nodes, run image embedding model if necessary.

    Args:
        nodes (Sequence[ImageNode]): The nodes to embed.
        embed_model (MultiModalEmbedding): The embedding model to use.
        show_progress (bool): Whether to show progress bar.

    Returns:
        Dict[str, List[float]]: A map from node id to embedding.
    """
    id_to_embed_map: Dict[str, List[float]] = {}

    images_to_embed = []
    ids_to_embed = []
    for node in nodes:
        if node.embedding is None:
            ids_to_embed.append(node.node_id)
            images_to_embed.append(node.resolve_image())
        else:
            id_to_embed_map[node.node_id] = node.embedding

    new_embeddings = embed_model.get_image_embedding_batch(
        images_to_embed, show_progress=show_progress
    )

    for new_id, img_embedding in zip(ids_to_embed, new_embeddings):
        id_to_embed_map[new_id] = img_embedding

    return id_to_embed_map

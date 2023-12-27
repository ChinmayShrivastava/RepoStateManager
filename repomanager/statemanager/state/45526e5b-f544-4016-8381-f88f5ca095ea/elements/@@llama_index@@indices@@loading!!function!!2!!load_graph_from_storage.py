def load_graph_from_storage(
    storage_context: StorageContext,
    root_id: str,
    **kwargs: Any,
) -> ComposableGraph:
    """Load composable graph from storage context.

    Args:
        storage_context (StorageContext): storage context containing
            docstore, index store and vector store.
        root_id (str): ID of the root index of the graph.
        **kwargs: Additional keyword args to pass to the index constructors.
    """
    indices = load_indices_from_storage(storage_context, index_ids=None, **kwargs)
    all_indices = {index.index_id: index for index in indices}
    return ComposableGraph(all_indices=all_indices, root_id=root_id)

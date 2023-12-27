def load_index(root: str = ".") -> BaseIndex[Any]:
    """Load existing index file."""
    config = load_config(root)
    service_context = _load_service_context(config)

    # Index type
    index_type: Type
    if config["index"]["type"] == "default" or config["index"]["type"] == "vector":
        index_type = VectorStoreIndex
    elif config["index"]["type"] == "keyword":
        index_type = SimpleKeywordTableIndex
    else:
        raise KeyError(f"Unknown index.type {config['index']['type']}")

    try:
        # try loading index
        storage_context = _load_storage_context(config)
        index = load_index_from_storage(storage_context)
    except ValueError:
        # build index
        storage_context = StorageContext.from_defaults()
        index = index_type(
            nodes=[], service_context=service_context, storage_context=storage_context
        )
    return index

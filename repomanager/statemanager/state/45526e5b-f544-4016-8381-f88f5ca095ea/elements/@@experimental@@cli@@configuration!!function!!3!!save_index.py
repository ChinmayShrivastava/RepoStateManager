def save_index(index: BaseIndex[Any], root: str = ".") -> None:
    """Save index to file."""
    config = load_config(root)
    persist_dir = config["store"]["persist_dir"]
    index.storage_context.persist(persist_dir=persist_dir)

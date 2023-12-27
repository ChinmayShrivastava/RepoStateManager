def _load_storage_context(config: ConfigParser) -> StorageContext:
    persist_dir = config["store"]["persist_dir"]
    return StorageContext.from_defaults(persist_dir=persist_dir)

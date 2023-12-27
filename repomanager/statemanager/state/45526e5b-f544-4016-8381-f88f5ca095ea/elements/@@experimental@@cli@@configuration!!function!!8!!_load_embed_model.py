def _load_embed_model(config: ConfigParser) -> BaseEmbedding:
    """Internal function to load embedding model based on configuration."""
    model_type = config["embed_model"]["type"]
    if model_type == "default":
        return OpenAIEmbedding()
    else:
        raise KeyError("embed_model.type")

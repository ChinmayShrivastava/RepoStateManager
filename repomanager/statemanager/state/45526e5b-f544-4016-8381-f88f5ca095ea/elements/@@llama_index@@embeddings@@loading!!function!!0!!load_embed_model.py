def load_embed_model(data: dict) -> BaseEmbedding:
    """Load Embedding by name."""
    if isinstance(data, BaseEmbedding):
        return data
    name = data.get("class_name", None)
    if name is None:
        raise ValueError("Embedding loading requires a class_name")
    if name not in RECOGNIZED_EMBEDDINGS:
        raise ValueError(f"Invalid Embedding name: {name}")

    # special handling for LangchainEmbedding
    # it can be any local model technially
    if name == LangchainEmbedding.class_name():
        local_name = data.get("model_name", None)
        if local_name is not None:
            return resolve_embed_model("local:" + local_name)
        else:
            raise ValueError("LangchainEmbedding requires a model_name")

    return RECOGNIZED_EMBEDDINGS[name].from_dict(data)

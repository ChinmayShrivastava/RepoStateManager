def create_local_embedding(
    model_name: str, batch_size: int
) -> Tuple[BaseEmbedding, str, int]:
    model = resolve_embed_model(f"local:{model_name}")
    return (
        model,
        "hf/" + model_name,
        model._langchain_embedding.client.max_seq_length,  # type: ignore
    )

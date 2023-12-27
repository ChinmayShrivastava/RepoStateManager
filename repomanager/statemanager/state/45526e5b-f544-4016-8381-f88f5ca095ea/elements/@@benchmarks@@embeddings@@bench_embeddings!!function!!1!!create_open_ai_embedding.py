def create_open_ai_embedding(batch_size: int) -> Tuple[BaseEmbedding, str, int]:
    return (
        OpenAIEmbedding(embed_batch_size=batch_size),
        "OpenAIEmbedding",
        4096,
    )

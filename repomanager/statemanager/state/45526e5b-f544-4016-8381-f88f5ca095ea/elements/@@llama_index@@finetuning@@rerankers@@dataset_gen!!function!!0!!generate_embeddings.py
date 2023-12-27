def generate_embeddings(embed_model: Any, text: str) -> List[float]:
    # Generate embeddings for a list of texts
    return embed_model.get_text_embedding(text)

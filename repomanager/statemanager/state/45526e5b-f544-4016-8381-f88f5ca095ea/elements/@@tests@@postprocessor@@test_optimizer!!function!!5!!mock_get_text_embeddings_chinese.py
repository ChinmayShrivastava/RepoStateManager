def mock_get_text_embeddings_chinese(texts: List[str]) -> List[List[float]]:
    """Mock get text embeddings."""
    return [mock_get_text_embedding_chinese(text) for text in texts]

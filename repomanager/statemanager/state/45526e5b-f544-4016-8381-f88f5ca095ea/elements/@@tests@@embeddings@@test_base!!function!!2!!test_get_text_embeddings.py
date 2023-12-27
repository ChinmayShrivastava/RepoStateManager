def test_get_text_embeddings(
    _mock_get_text_embeddings: Any, _mock_get_text_embedding: Any
) -> None:
    """Test get queued text embeddings."""
    embed_model = OpenAIEmbedding(embed_batch_size=8)
    texts_to_embed = []
    for i in range(8):
        texts_to_embed.append("Hello world.")
    for i in range(8):
        texts_to_embed.append("This is a test.")
    for i in range(4):
        texts_to_embed.append("This is another test.")
    for i in range(4):
        texts_to_embed.append("This is a test v2.")

    result_embeddings = embed_model.get_text_embedding_batch(texts_to_embed)
    for i in range(8):
        assert result_embeddings[i] == [1, 0, 0, 0, 0]
    for i in range(8, 16):
        assert result_embeddings[i] == [0, 1, 0, 0, 0]
    for i in range(16, 20):
        assert result_embeddings[i] == [0, 0, 1, 0, 0]
    for i in range(20, 24):
        assert result_embeddings[i] == [0, 0, 0, 1, 0]

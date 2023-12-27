def test_fastembed_query_embedding(model_name: str, max_length: int) -> None:
    """Test FastEmbed batch embedding."""
    query = "foo bar"
    embedding = FastEmbedEmbedding(
        model_name=model_name,
        max_length=max_length,
    )

    output = embedding.get_query_embedding(query)
    assert len(output) == 384

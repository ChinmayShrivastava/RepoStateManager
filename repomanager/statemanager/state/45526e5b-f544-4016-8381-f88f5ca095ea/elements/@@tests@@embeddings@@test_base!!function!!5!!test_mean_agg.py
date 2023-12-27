def test_mean_agg() -> None:
    """Test mean aggregation for embeddings."""
    embedding_0 = [3.0, 4.0, 0.0]
    embedding_1 = [0.0, 1.0, 0.0]
    output = mean_agg([embedding_0, embedding_1])
    assert output == [1.5, 2.5, 0.0]

def test_embedding_similarity_euclidean() -> None:
    embed_model = OpenAIEmbedding()
    query_embedding = [1.0, 0.0]
    text1_embedding = [0.0, 1.0]  # further from query_embedding distance=1.414
    text2_embedding = [1.0, 1.0]  # closer to query_embedding distance=1.0
    euclidean_similarity1 = embed_model.similarity(
        query_embedding, text1_embedding, mode=SimilarityMode.EUCLIDEAN
    )
    euclidean_similarity2 = embed_model.similarity(
        query_embedding, text2_embedding, mode=SimilarityMode.EUCLIDEAN
    )
    assert euclidean_similarity1 < euclidean_similarity2

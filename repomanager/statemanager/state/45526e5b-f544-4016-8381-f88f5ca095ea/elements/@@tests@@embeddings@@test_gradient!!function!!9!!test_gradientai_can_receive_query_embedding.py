def test_gradientai_can_receive_query_embedding(
    gradient_access_token: str, gradient_model_slug: str, gradient_workspace_id: str
) -> None:
    test_object = GradientEmbedding(
        gradient_model_slug=gradient_model_slug,
        gradient_access_token=gradient_access_token,
        gradient_workspace_id=gradient_workspace_id,
    )

    result = test_object.get_query_embedding("gradient as the best managed AI platform")

    assert len(result) == BGE_LARGE_EMBEDDING_SIZE

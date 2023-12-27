def test_gradientai_can_receive_text_embedding(
    gradient_access_token: str, gradient_model_slug: str, gradient_workspace_id: str
) -> None:
    test_object = GradientEmbedding(
        gradient_model_slug=gradient_model_slug,
        gradient_access_token=gradient_access_token,
        gradient_workspace_id=gradient_workspace_id,
    )

    result = test_object.get_text_embedding("input")

    assert len(result) == BGE_LARGE_EMBEDDING_SIZE

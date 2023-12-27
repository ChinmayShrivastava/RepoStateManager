def test_gradientai_can_receive_multiple_text_embeddings(
    gradient_access_token: str, gradient_model_slug: str, gradient_workspace_id: str
) -> None:
    test_object = GradientEmbedding(
        gradient_model_slug=gradient_model_slug,
        gradient_access_token=gradient_access_token,
        gradient_workspace_id=gradient_workspace_id,
    )

    inputs = ["first input", "second input"]
    result = test_object.get_text_embedding_batch(inputs)

    assert len(result) == len(inputs)
    assert len(result[0]) == BGE_LARGE_EMBEDDING_SIZE
    assert len(result[1]) == BGE_LARGE_EMBEDDING_SIZE

def test_gradientai_embedding_constructor(
    gradient_access_token: str, gradient_model_slug: str, gradient_workspace_id: str
) -> None:
    """Test Gradient AI embedding query."""
    test_object = GradientEmbedding(
        gradient_model_slug=gradient_model_slug,
        gradient_access_token=gradient_access_token,
        gradient_workspace_id=gradient_workspace_id,
    )
    assert test_object is not None

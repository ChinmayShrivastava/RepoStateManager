def test_gradientai_throws_without_proper_auth(
    gradient_model_slug: str, gradient_workspace_id: str
) -> None:
    """Test Gradient AI embedding query."""
    with pytest.raises(ValueError):
        GradientEmbedding(
            gradient_model_slug=gradient_model_slug,
            gradient_access_token="definitely-not-a-valid-token",
            gradient_workspace_id=gradient_workspace_id,
        )

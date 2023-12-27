def test_gradientai_throws_if_not_installed(
    gradient_access_token: str, gradient_model_slug: str, gradient_workspace_id: str
) -> None:
    with pytest.raises(ImportError):
        GradientEmbedding(
            gradient_model_slug=gradient_model_slug,
            gradient_access_token=gradient_access_token,
            gradient_workspace_id=gradient_workspace_id,
        )

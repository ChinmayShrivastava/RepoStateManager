def test_gradientai_cannot_support_batches_larger_than_100(
    gradient_access_token: str, gradient_model_slug: str, gradient_workspace_id: str
) -> None:
    with pytest.raises(ValueError):
        GradientEmbedding(
            embed_batch_size=101,
            gradient_model_slug=gradient_model_slug,
            gradient_access_token=gradient_access_token,
            gradient_workspace_id=gradient_workspace_id,
        )

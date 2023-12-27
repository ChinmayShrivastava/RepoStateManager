def test_gradient_base() -> None:
    """Test Gradient."""
    # Set up fake package here
    with patch.dict(sys.modules, {"gradientai": MockGradientaiPackage()}):
        n_tokens = 2
        gradientllm = GradientBaseModelLLM(
            access_token="dummy-token",
            base_model_slug="dummy-base-model",
            workspace_id="dummy-workspace",
            max_tokens=n_tokens,
        )
        response = gradientllm.complete("hello world")
        assert isinstance(response, CompletionResponse)
        assert response.text == "hello world" * n_tokens

def test_gradient_adapter() -> None:
    # Set up fake package here
    with patch.dict(sys.modules, {"gradientai": MockGradientaiPackage()}):
        n_tokens = 5
        gradientllm = GradientModelAdapterLLM(
            access_token="dummy-token",
            model_adapter_id="dummy-adapter-model",
            workspace_id="dummy-workspace",
            max_tokens=n_tokens,
        )
        response = gradientllm.complete("hello world")
        assert isinstance(response, CompletionResponse)
        assert response.text == "hello world" * n_tokens

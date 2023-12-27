def test_palm() -> None:
    """Test palm."""
    # Set up fake package here, as test_gemini uses the same package.
    sys.modules["google.generativeai"] = MockPalmPackage()

    palm = PaLM(api_key="test_api_key", model_name="palm_model")
    response = palm.complete("hello world")
    assert isinstance(response, CompletionResponse)
    assert response.text == "hello world"

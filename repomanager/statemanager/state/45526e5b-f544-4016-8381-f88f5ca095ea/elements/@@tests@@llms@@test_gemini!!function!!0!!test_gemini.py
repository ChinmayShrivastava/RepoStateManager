def test_gemini() -> None:
    # Set up fake package here, as test_palm uses the same package.
    sys.modules["google.generativeai"] = MockGenaiPackage()

    MockGenaiPackage.response_text = "echo echo"

    llm = Gemini(model_name="models/one")
    response = llm.complete("say echo")

    assert isinstance(response, CompletionResponse)
    assert response.text == "echo echo"

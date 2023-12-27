def test_predict__basic(
    mock_vellum_client_factory: Callable[..., mock.MagicMock],
    vellum_predictor_factory: Callable[..., VellumPredictor],
    dummy_prompt: BasePromptTemplate,
) -> None:
    """When the Vellum API returns expected values, so should our predictor."""
    vellum_client = mock_vellum_client_factory(
        compiled_prompt_text="What's you're favorite greeting?",
        completion_text="Hello, world!",
    )

    predictor = vellum_predictor_factory(vellum_client=vellum_client)

    completion_text = predictor.predict(dummy_prompt, thing="greeting")

    assert completion_text == "Hello, world!"

def test_get_compiled_prompt__basic(
    mock_vellum_client_factory: Callable[..., mock.MagicMock],
    vellum_prompt_registry_factory: Callable[..., VellumPromptRegistry],
) -> None:
    """Verify that we can get a compiled prompt from the registry."""
    registered_prompt = VellumRegisteredPrompt(
        deployment_id="abc",
        deployment_name="my-deployment",
        model_version_id="123",
    )

    vellum_client = mock_vellum_client_factory()
    mock_model_version_compile_prompt = mock.MagicMock()
    mock_model_version_compile_prompt.prompt.text = "What's your favorite greeting?"
    mock_model_version_compile_prompt.prompt.num_tokens = 5

    vellum_client.model_versions.model_version_compile_prompt.return_value = (
        mock_model_version_compile_prompt
    )

    prompt_registry = vellum_prompt_registry_factory(vellum_client=vellum_client)

    compiled_prompt = prompt_registry.get_compiled_prompt(
        registered_prompt, input_values={"thing": "greeting"}
    )

    assert compiled_prompt == VellumCompiledPrompt(
        text="What's your favorite greeting?", num_tokens=5
    )

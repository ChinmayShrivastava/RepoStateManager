def test_from_prompt__new(
    mock_vellum_client_factory: Callable[..., mock.MagicMock],
    vellum_prompt_registry_factory: Callable[..., VellumPromptRegistry],
) -> None:
    """We should register a new prompt if no deployment exists."""
    from vellum.core import ApiError

    dummy_prompt = PromptTemplate(template="What's your favorite {thing}?")

    vellum_client = mock_vellum_client_factory()

    vellum_client.deployments.retrieve.side_effect = ApiError(status_code=404)

    prompt_registry = vellum_prompt_registry_factory(vellum_client=vellum_client)
    prompt_registry.from_prompt(dummy_prompt)

    vellum_client.registered_prompts.register_prompt.assert_called_once()

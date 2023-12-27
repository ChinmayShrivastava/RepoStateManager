def test_from_prompt__existing(
    mock_vellum_client_factory: Callable[..., mock.MagicMock],
    vellum_prompt_registry_factory: Callable[..., VellumPromptRegistry],
) -> None:
    """We shouldn't register a new prompt if a deployment id or name is provided."""
    dummy_prompt = PromptTemplate(
        template="What's your favorite {thing}?",
        metadata={"vellum_deployment_id": "abc"},
    )

    mock_deployment = mock.MagicMock(active_model_version_ids=["abc"])

    vellum_client = mock_vellum_client_factory()
    vellum_client.deployments = mock.MagicMock()
    vellum_client.deployments.retrieve.return_value = mock_deployment

    prompt_registry = vellum_prompt_registry_factory(vellum_client=vellum_client)
    prompt_registry.from_prompt(dummy_prompt)

    vellum_client.registered_prompts.register_prompt.assert_not_called()

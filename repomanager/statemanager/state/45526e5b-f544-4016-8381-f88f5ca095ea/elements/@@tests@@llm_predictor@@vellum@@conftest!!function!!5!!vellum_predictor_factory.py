def vellum_predictor_factory(
    fake_vellum_api_key: str,
    mock_vellum_client_factory: Callable[..., mock.MagicMock],
    mock_vellum_async_client_factory: Callable[..., mock.MagicMock],
    vellum_prompt_registry_factory: Callable[..., mock.MagicMock],
) -> Callable[..., VellumPredictor]:
    def _create_vellum_predictor(
        callback_manager: Optional[CallbackManager] = None,
        vellum_client: Optional[mock.MagicMock] = None,
        async_vellum_client: Optional[mock.MagicMock] = None,
        vellum_prompt_registry: Optional[mock.MagicMock] = None,
    ) -> VellumPredictor:
        predictor = VellumPredictor(
            vellum_api_key=fake_vellum_api_key, callback_manager=callback_manager
        )

        vellum_client = vellum_client or mock_vellum_client_factory()
        async_vellum_client = async_vellum_client or mock_vellum_async_client_factory()
        vellum_prompt_registry = (
            vellum_prompt_registry
            or vellum_prompt_registry_factory(vellum_client=vellum_client)
        )

        predictor._vellum_client = vellum_client
        predictor._async_vellum_client = async_vellum_client
        predictor._prompt_registry = vellum_prompt_registry

        return predictor

    return _create_vellum_predictor

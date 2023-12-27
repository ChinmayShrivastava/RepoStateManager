    def _create_vellum_prompt_registry(
        vellum_client: Optional[mock.MagicMock] = None,
    ) -> VellumPromptRegistry:
        prompt_registry = VellumPromptRegistry(vellum_api_key=fake_vellum_api_key)
        prompt_registry._vellum_client = vellum_client or mock_vellum_client_factory()

        return prompt_registry

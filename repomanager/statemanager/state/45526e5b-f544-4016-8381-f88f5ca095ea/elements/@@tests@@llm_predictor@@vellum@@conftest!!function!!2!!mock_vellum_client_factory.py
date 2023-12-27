def mock_vellum_client_factory() -> Callable[..., mock.MagicMock]:
    import vellum

    def _create_vellum_client(
        compiled_prompt_text: str = "<example-compiled-prompt-text>",
        compiled_prompt_num_tokens: int = 0,
        completion_text: str = "<example_completion>",
    ) -> mock.MagicMock:
        mocked_vellum_client = mock.MagicMock()

        mocked_vellum_client.model_versions.model_version_compile_prompt.return_value.prompt = vellum.ModelVersionCompiledPrompt(
            text=compiled_prompt_text, num_tokens=compiled_prompt_num_tokens
        )
        mocked_vellum_client.generate.return_value = vellum.GenerateResponse(
            results=[
                vellum.GenerateResult(
                    data=vellum.GenerateResultData(
                        completions=[
                            vellum.EnrichedNormalizedCompletion(
                                id="<example-generation-id>",
                                external_id=None,
                                text=completion_text,
                                model_version_id="<example-model-version-id>",
                            )
                        ]
                    ),
                    error=None,
                )
            ]
        )

        return mocked_vellum_client

    return _create_vellum_client

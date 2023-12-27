def mock_service_context(
    patch_token_text_splitter: Any, patch_llm_predictor: Any
) -> ServiceContext:
    return ServiceContext.from_defaults(embed_model=MockEmbedding())

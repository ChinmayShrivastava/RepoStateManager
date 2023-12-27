def _load_service_context(config: ConfigParser) -> ServiceContext:
    """Internal function to load service context based on configuration."""
    embed_model = _load_embed_model(config)
    llm_predictor = _load_llm_predictor(config)
    return ServiceContext.from_defaults(
        llm_predictor=llm_predictor, embed_model=embed_model
    )

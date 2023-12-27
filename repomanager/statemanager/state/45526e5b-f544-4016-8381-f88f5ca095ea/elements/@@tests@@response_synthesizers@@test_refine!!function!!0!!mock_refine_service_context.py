def mock_refine_service_context(patch_llm_predictor: Any) -> ServiceContext:
    cb_manager = CallbackManager([])
    return ServiceContext.from_defaults(
        llm_predictor=patch_llm_predictor,
        callback_manager=cb_manager,
    )

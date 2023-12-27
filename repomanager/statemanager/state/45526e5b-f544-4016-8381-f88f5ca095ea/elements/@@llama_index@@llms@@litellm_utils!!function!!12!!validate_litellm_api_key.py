def validate_litellm_api_key(
    api_key: Optional[str] = None, api_type: Optional[str] = None
) -> None:
    import litellm

    api_key = litellm.validate_environment()
    if api_key is None:
        raise ValueError(MISSING_API_KEY_ERROR_MESSAGE)

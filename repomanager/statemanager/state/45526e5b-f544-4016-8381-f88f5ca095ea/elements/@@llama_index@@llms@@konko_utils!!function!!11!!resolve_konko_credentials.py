def resolve_konko_credentials(
    konko_api_key: Optional[str] = None,
    openai_api_key: Optional[str] = None,
    api_type: Optional[str] = None,
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
) -> Tuple[str, str, str, str, str]:
    """ "Resolve KonkoAI credentials.

    The order of precedence is:
    1. param
    2. env
    3. konkoai module
    4. default
    """
    import konko

    # resolve from param or env
    konko_api_key = get_from_param_or_env(
        "konko_api_key", konko_api_key, "KONKO_API_KEY", ""
    )
    openai_api_key = get_from_param_or_env(
        "openai_api_key", openai_api_key, "OPENAI_API_KEY", ""
    )
    api_type = get_from_param_or_env("api_type", api_type, "KONKO_API_TYPE", "")
    api_base = DEFAULT_KONKO_API_BASE
    api_version = get_from_param_or_env(
        "api_version", api_version, "KONKO_API_VERSION", ""
    )

    # resolve from konko module or default
    konko_api_key = konko_api_key
    openai_api_key = openai_api_key
    api_type = api_type or DEFAULT_KONKO_API_TYPE
    api_base = api_base or konko.api_base or DEFAULT_KONKO_API_BASE
    api_version = api_version or DEFAULT_KONKO_API_VERSION

    if not konko_api_key:
        raise ValueError(MISSING_API_KEY_ERROR_MESSAGE)

    return konko_api_key, openai_api_key, api_type, api_base, api_version

def set_google_config(
    *,
    api_endpoint: Optional[str] = None,
    user_agent: Optional[str] = None,
    page_size: Optional[int] = None,
    auth_credentials: Optional["credentials.Credentials"] = None,
    **kwargs: Any,
) -> None:
    """
    Set the configuration for Google Generative AI API.

    Parameters are optional, Normally, the defaults should work fine.
    If provided, they will override the default values in the Config class.
    See the docstring in `genai_extension.py` for more details.
    auth_credentials: Optional["credentials.Credentials"] = None,
    Use this to pass Google Auth credentials such as using a service account.
    Refer to for auth credentials documentation:
    https://developers.google.com/identity/protocols/oauth2/service-account#creatinganaccount.

    Example:
        from google.oauth2 import service_account
        credentials = service_account.Credentials.from_service_account_file(
            "/path/to/service.json",
            scopes=[
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/generative-language.retriever",
            ],
        )
        set_google_config(auth_credentials=credentials)
    """
    try:
        import llama_index.vector_stores.google.generativeai.genai_extension as genaix
    except ImportError:
        raise ImportError(_import_err_msg)

    config_attrs = {
        "api_endpoint": api_endpoint,
        "user_agent": user_agent,
        "page_size": page_size,
        "auth_credentials": auth_credentials,
        "testing": kwargs.get("testing", None),
    }
    attrs = {k: v for k, v in config_attrs.items() if v is not None}
    config = genaix.Config(**attrs)
    genaix.set_config(config)

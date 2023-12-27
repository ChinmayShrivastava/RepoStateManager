class Config:
    """Global configuration for Google Generative AI API.

    Normally, the defaults should work fine. Use this to pass Google Auth credentials
    such as using a service account. Refer to for auth credentials documentation:
    https://developers.google.com/identity/protocols/oauth2/service-account#creatinganaccount.

    Attributes:
        api_endpoint: The Google Generative API endpoint address.
        user_agent: The user agent to use for logging.
        page_size: For paging RPCs, how many entities to return per RPC.
        testing: Are the unit tests running?
        auth_credentials: For setting credentials such as using service accounts.
    """

    api_endpoint: str = _DEFAULT_API_ENDPOINT
    user_agent: str = _USER_AGENT
    page_size: int = _DEFAULT_PAGE_SIZE
    testing: bool = False
    auth_credentials: Optional[credentials.Credentials] = None

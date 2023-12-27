def refresh_openai_azuread_token(
    azure_ad_token: Any = None,
) -> Any:
    """
    Checks the validity of the associated token, if any, and tries to refresh it
    using the credentials available in the current context. Different authentication
    methods are tried, in order, until a successful one is found as defined at the
    package `azure-indentity`.
    """
    try:
        from azure.core.exceptions import ClientAuthenticationError
        from azure.identity import DefaultAzureCredential
    except ImportError as ex:
        raise ValueError(
            "Using API type `azure_ad` or `azuread` requires the package"
            " `azure-identity` to be installed."
        ) from ex

    if not azure_ad_token or azure_ad_token.expires_on < time.time() + 60:
        try:
            credential = DefaultAzureCredential()
            azure_ad_token = credential.get_token(
                "https://cognitiveservices.azure.com/.default"
            )
        except ClientAuthenticationError as err:
            raise ValueError(
                "Unable to acquire a valid Microsoft Entra ID (former Azure AD) token for "
                f"the resource due to the following error: {err.message}"
            ) from err
    return azure_ad_token

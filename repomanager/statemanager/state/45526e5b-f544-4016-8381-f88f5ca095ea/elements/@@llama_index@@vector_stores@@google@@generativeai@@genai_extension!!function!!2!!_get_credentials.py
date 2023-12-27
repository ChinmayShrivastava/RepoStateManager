def _get_credentials() -> Optional[credentials.Credentials]:
    """Returns a credential from the config if set or a fake credentials for unit testing.

    If _config.testing is True, a fake credential is returned.
    Otherwise, we are in a real environment and will use credentials if provided or None is returned.

    If None is passed to the clients later on, the actual credentials will be
    inferred by the rules specified in google.auth package.
    """
    if _config.testing:
        return TestCredentials()
    elif _config.auth_credentials:
        return _config.auth_credentials
    return None

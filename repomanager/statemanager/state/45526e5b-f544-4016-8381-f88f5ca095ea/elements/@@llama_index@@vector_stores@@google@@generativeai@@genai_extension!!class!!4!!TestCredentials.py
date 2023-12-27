class TestCredentials(credentials.Credentials):
    """Credentials that do not provide any authentication information.

    Useful for unit tests where the credentials are not used.
    """

    @property
    def expired(self) -> bool:
        """Returns `False`, test credentials never expire."""
        return False

    @property
    def valid(self) -> bool:
        """Returns `True`, test credentials are always valid."""
        return True

    def refresh(self, request: Any) -> None:
        """Raises :class:``InvalidOperation``, test credentials cannot be
        refreshed.
        """
        raise exceptions.InvalidOperation("Test credentials cannot be refreshed.")

    def apply(self, headers: Any, token: Any = None) -> None:
        """Anonymous credentials do nothing to the request.

        The optional ``token`` argument is not supported.

        Raises:
            google.auth.exceptions.InvalidValue: If a token was specified.
        """
        if token is not None:
            raise exceptions.InvalidValue("Test credentials don't support tokens.")

    def before_request(self, request: Any, method: Any, url: Any, headers: Any) -> None:
        """Test credentials do nothing to the request."""

class BaseClientWrapper:
    def __init__(self, *, token: typing.Optional[typing.Union[str, typing.Callable[[], str]]] = None, base_url: str):
        self._token = token
        self._base_url = base_url

    def get_headers(self) -> typing.Dict[str, str]:
        headers: typing.Dict[str, str] = {
            "X-Fern-Language": "Python",
            "X-Fern-SDK-Name": "superagent-py",
            "X-Fern-SDK-Version": "v0.1.48",
        }
        token = self._get_token()
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def _get_token(self) -> typing.Optional[str]:
        if isinstance(self._token, str) or self._token is None:
            return self._token
        else:
            return self._token()

    def get_base_url(self) -> str:
        return self._base_url

class AsyncClientWrapper(BaseClientWrapper):
    def __init__(
        self,
        *,
        token: typing.Optional[typing.Union[str, typing.Callable[[], str]]] = None,
        base_url: str,
        httpx_client: httpx.AsyncClient,
    ):
        super().__init__(token=token, base_url=base_url)
        self.httpx_client = httpx_client

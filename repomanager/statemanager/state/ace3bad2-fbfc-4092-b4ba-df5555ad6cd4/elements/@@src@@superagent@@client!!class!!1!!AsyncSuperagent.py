class AsyncSuperagent:
    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: SuperagentEnvironment = SuperagentEnvironment.DEFAULT,
        token: typing.Optional[typing.Union[str, typing.Callable[[], str]]] = None,
        timeout: typing.Optional[float] = 60,
        httpx_client: typing.Optional[httpx.AsyncClient] = None
    ):
        self._client_wrapper = AsyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            token=token,
            httpx_client=httpx.AsyncClient(timeout=timeout) if httpx_client is None else httpx_client,
        )
        self.agent = AsyncAgentClient(client_wrapper=self._client_wrapper)
        self.llm = AsyncLlmClient(client_wrapper=self._client_wrapper)
        self.api_user = AsyncApiUserClient(client_wrapper=self._client_wrapper)
        self.datasource = AsyncDatasourceClient(client_wrapper=self._client_wrapper)
        self.tool = AsyncToolClient(client_wrapper=self._client_wrapper)
        self.workflow = AsyncWorkflowClient(client_wrapper=self._client_wrapper)

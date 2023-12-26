class Superagent:
    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: SuperagentEnvironment = SuperagentEnvironment.DEFAULT,
        token: typing.Optional[typing.Union[str, typing.Callable[[], str]]] = None,
        timeout: typing.Optional[float] = 60,
        httpx_client: typing.Optional[httpx.Client] = None
    ):
        self._client_wrapper = SyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            token=token,
            httpx_client=httpx.Client(timeout=timeout) if httpx_client is None else httpx_client,
        )
        self.agent = AgentClient(client_wrapper=self._client_wrapper)
        self.llm = LlmClient(client_wrapper=self._client_wrapper)
        self.api_user = ApiUserClient(client_wrapper=self._client_wrapper)
        self.datasource = DatasourceClient(client_wrapper=self._client_wrapper)
        self.tool = ToolClient(client_wrapper=self._client_wrapper)
        self.workflow = WorkflowClient(client_wrapper=self._client_wrapper)

class OpenAIEmbedding(BaseEmbedding):
    """OpenAI class for embeddings.

    Args:
        mode (str): Mode for embedding.
            Defaults to OpenAIEmbeddingMode.TEXT_SEARCH_MODE.
            Options are:

            - OpenAIEmbeddingMode.SIMILARITY_MODE
            - OpenAIEmbeddingMode.TEXT_SEARCH_MODE

        model (str): Model for embedding.
            Defaults to OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002.
            Options are:

            - OpenAIEmbeddingModelType.DAVINCI
            - OpenAIEmbeddingModelType.CURIE
            - OpenAIEmbeddingModelType.BABBAGE
            - OpenAIEmbeddingModelType.ADA
            - OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002
    """

    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs for the OpenAI API."
    )

    api_key: str = Field(description="The OpenAI API key.")
    api_base: str = Field(description="The base URL for OpenAI API.")
    api_version: str = Field(description="The version for OpenAI API.")

    max_retries: int = Field(
        default=10, description="Maximum number of retries.", gte=0
    )
    timeout: float = Field(default=60.0, description="Timeout for each request.", gte=0)
    default_headers: Optional[Dict[str, str]] = Field(
        default=None, description="The default headers for API requests."
    )
    reuse_client: bool = Field(
        default=True,
        description=(
            "Reuse the OpenAI client between requests. When doing anything with large "
            "volumes of async API calls, setting this to false can improve stability."
        ),
    )

    _query_engine: OpenAIEmbeddingModeModel = PrivateAttr()
    _text_engine: OpenAIEmbeddingModeModel = PrivateAttr()
    _client: Optional[OpenAI] = PrivateAttr()
    _aclient: Optional[AsyncOpenAI] = PrivateAttr()
    _http_client: Optional[httpx.Client] = PrivateAttr()

    def __init__(
        self,
        mode: str = OpenAIEmbeddingMode.TEXT_SEARCH_MODE,
        model: str = OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        api_version: Optional[str] = None,
        max_retries: int = 10,
        timeout: float = 60.0,
        reuse_client: bool = True,
        callback_manager: Optional[CallbackManager] = None,
        default_headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.Client] = None,
        **kwargs: Any,
    ) -> None:
        additional_kwargs = additional_kwargs or {}

        api_key, api_base, api_version = resolve_openai_credentials(
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
        )

        self._query_engine = get_engine(mode, model, _QUERY_MODE_MODEL_DICT)
        self._text_engine = get_engine(mode, model, _TEXT_MODE_MODEL_DICT)

        if "model_name" in kwargs:
            model_name = kwargs.pop("model_name")
        else:
            model_name = model

        super().__init__(
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,
            model_name=model_name,
            additional_kwargs=additional_kwargs,
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
            max_retries=max_retries,
            reuse_client=reuse_client,
            timeout=timeout,
            default_headers=default_headers,
            **kwargs,
        )

        self._client = None
        self._aclient = None
        self._http_client = http_client

    def _get_client(self) -> OpenAI:
        if not self.reuse_client:
            return OpenAI(**self._get_credential_kwargs())

        if self._client is None:
            self._client = OpenAI(**self._get_credential_kwargs())
        return self._client

    def _get_aclient(self) -> AsyncOpenAI:
        if not self.reuse_client:
            return AsyncOpenAI(**self._get_credential_kwargs())

        if self._aclient is None:
            self._aclient = AsyncOpenAI(**self._get_credential_kwargs())
        return self._aclient

    @classmethod
    def class_name(cls) -> str:
        return "OpenAIEmbedding"

    def _get_credential_kwargs(self) -> Dict[str, Any]:
        return {
            "api_key": self.api_key,
            "base_url": self.api_base,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "default_headers": self.default_headers,
            "http_client": self._http_client,
        }

    def _get_query_embedding(self, query: str) -> List[float]:
        """Get query embedding."""
        client = self._get_client()
        return get_embedding(
            client,
            query,
            engine=self._query_engine,
            **self.additional_kwargs,
        )

    async def _aget_query_embedding(self, query: str) -> List[float]:
        """The asynchronous version of _get_query_embedding."""
        aclient = self._get_aclient()
        return await aget_embedding(
            aclient,
            query,
            engine=self._query_engine,
            **self.additional_kwargs,
        )

    def _get_text_embedding(self, text: str) -> List[float]:
        """Get text embedding."""
        client = self._get_client()
        return get_embedding(
            client,
            text,
            engine=self._text_engine,
            **self.additional_kwargs,
        )

    async def _aget_text_embedding(self, text: str) -> List[float]:
        """Asynchronously get text embedding."""
        aclient = self._get_aclient()
        return await aget_embedding(
            aclient,
            text,
            engine=self._text_engine,
            **self.additional_kwargs,
        )

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get text embeddings.

        By default, this is a wrapper around _get_text_embedding.
        Can be overridden for batch queries.

        """
        client = self._get_client()
        return get_embeddings(
            client,
            texts,
            engine=self._text_engine,
            **self.additional_kwargs,
        )

    async def _aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Asynchronously get text embeddings."""
        aclient = self._get_aclient()
        return await aget_embeddings(
            aclient,
            texts,
            engine=self._text_engine,
            **self.additional_kwargs,
        )

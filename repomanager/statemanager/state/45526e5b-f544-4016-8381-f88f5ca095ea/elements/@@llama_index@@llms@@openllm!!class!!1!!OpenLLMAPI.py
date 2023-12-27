class OpenLLMAPI(LLM):
    """OpenLLM Client interface. This is useful when interacting with a remote OpenLLM server."""

    address: Optional[str] = Field(
        description="OpenLLM server address. This could either be set here or via OPENLLM_ENDPOINT"
    )
    timeout: int = Field(description="Timeout for sending requests.")
    max_retries: int = Field(description="Maximum number of retries.")
    api_version: Literal["v1"] = Field(description="OpenLLM Server API version.")

    if TYPE_CHECKING:
        try:
            from openllm_client import AsyncHTTPClient, HTTPClient

            _sync_client: HTTPClient
            _async_client: AsyncHTTPClient
        except ImportError:
            _sync_client: Any  # type: ignore[no-redef]
            _async_client: Any  # type: ignore[no-redef]
    else:
        _sync_client: Any = PrivateAttr()
        _async_client: Any = PrivateAttr()

    def __init__(
        self,
        address: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 2,
        api_version: Literal["v1"] = "v1",
        **kwargs: Any,
    ):
        try:
            from openllm_client import AsyncHTTPClient, HTTPClient
        except ImportError:
            raise ImportError(
                f'"{type(self).__name__}" requires "openllm-client". Make sure to install with `pip install openllm-client`'
            )
        super().__init__(
            address=address,
            timeout=timeout,
            max_retries=max_retries,
            api_version=api_version,
            **kwargs,
        )
        self._sync_client = HTTPClient(
            address=address,
            timeout=timeout,
            max_retries=max_retries,
            api_version=api_version,
        )
        self._async_client = AsyncHTTPClient(
            address=address,
            timeout=timeout,
            max_retries=max_retries,
            api_version=api_version,
        )

    @classmethod
    def class_name(cls) -> str:
        return "OpenLLM_Client"

    @property
    def _server_metadata(self) -> "Metadata":
        return self._sync_client._metadata

    @property
    def _server_config(self) -> Dict[str, Any]:
        return self._sync_client._config

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            num_output=self._server_config["max_new_tokens"],
            model_name=self._server_metadata.model_id.replace("/", "--"),
        )

    def _convert_messages_to_prompt(self, messages: Sequence[ChatMessage]) -> str:
        return self._sync_client.helpers.messages(
            messages=[
                {"role": message.role, "content": message.content}
                for message in messages
            ],
            add_generation_prompt=True,
        )

    async def _async_messages_to_prompt(self, messages: Sequence[ChatMessage]) -> str:
        return await self._async_client.helpers.messages(
            messages=[
                {"role": message.role, "content": message.content}
                for message in messages
            ],
            add_generation_prompt=True,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        response = self._sync_client.generate(prompt, **kwargs)
        return CompletionResponse(
            text=response.outputs[0].text,
            raw=response.model_dump(),
            additional_kwargs={
                "prompt_token_ids": response.prompt_token_ids,
                "prompt_logprobs": response.prompt_logprobs,
                "finished": response.finished,
                "outputs": {
                    "token_ids": response.outputs[0].token_ids,
                    "cumulative_logprob": response.outputs[0].cumulative_logprob,
                    "logprobs": response.outputs[0].logprobs,
                    "finish_reason": response.outputs[0].finish_reason,
                },
            },
        )

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        for response_chunk in self._sync_client.generate_stream(prompt, **kwargs):
            yield CompletionResponse(
                text=response_chunk.text,
                delta=response_chunk.text,
                raw=response_chunk.model_dump(),
                additional_kwargs={"token_ids": response_chunk.token_ids},
            )

    @llm_chat_callback()
    def chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        return completion_response_to_chat_response(
            self.complete(self._convert_messages_to_prompt(messages), **kwargs)
        )

    @llm_chat_callback()
    def stream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        for response_chunk in self.stream_complete(
            self._convert_messages_to_prompt(messages), **kwargs
        ):
            yield completion_response_to_chat_response(response_chunk)

    @llm_completion_callback()
    async def acomplete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        response = await self._async_client.generate(prompt, **kwargs)
        return CompletionResponse(
            text=response.outputs[0].text,
            raw=response.model_dump(),
            additional_kwargs={
                "prompt_token_ids": response.prompt_token_ids,
                "prompt_logprobs": response.prompt_logprobs,
                "finished": response.finished,
                "outputs": {
                    "token_ids": response.outputs[0].token_ids,
                    "cumulative_logprob": response.outputs[0].cumulative_logprob,
                    "logprobs": response.outputs[0].logprobs,
                    "finish_reason": response.outputs[0].finish_reason,
                },
            },
        )

    @llm_completion_callback()
    async def astream_complete(
        self, prompt: str, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        async for response_chunk in self._async_client.generate_stream(
            prompt, **kwargs
        ):
            yield CompletionResponse(
                text=response_chunk.text,
                delta=response_chunk.text,
                raw=response_chunk.model_dump(),
                additional_kwargs={"token_ids": response_chunk.token_ids},
            )

    @llm_chat_callback()
    async def achat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        return completion_response_to_chat_response(
            await self.acomplete(
                await self._async_messages_to_prompt(messages), **kwargs
            )
        )

    @llm_chat_callback()
    async def astream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        async for response_chunk in self.astream_complete(
            await self._async_messages_to_prompt(messages), **kwargs
        ):
            yield completion_response_to_chat_response(response_chunk)

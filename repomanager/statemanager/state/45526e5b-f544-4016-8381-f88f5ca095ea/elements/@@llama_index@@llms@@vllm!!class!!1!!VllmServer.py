class VllmServer(Vllm):
    def __init__(
        self,
        model: str = "facebook/opt-125m",
        api_url: str = "http://localhost:8000",
        temperature: float = 1.0,
        tensor_parallel_size: Optional[int] = 1,
        trust_remote_code: Optional[bool] = True,
        n: int = 1,
        best_of: Optional[int] = None,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        top_p: float = 1.0,
        top_k: int = -1,
        use_beam_search: bool = False,
        stop: Optional[List[str]] = None,
        ignore_eos: bool = False,
        max_new_tokens: int = 512,
        logprobs: Optional[int] = None,
        dtype: str = "auto",
        download_dir: Optional[str] = None,
        messages_to_prompt: Optional[Callable] = None,
        completion_to_prompt: Optional[Callable] = None,
        vllm_kwargs: Dict[str, Any] = {},
        callback_manager: Optional[CallbackManager] = None,
        output_parser: Optional[BaseOutputParser] = None,
    ) -> None:
        self._client = None
        messages_to_prompt = messages_to_prompt or generic_messages_to_prompt
        completion_to_prompt = completion_to_prompt or (lambda x: x)
        callback_manager = callback_manager or CallbackManager([])

        model = ""
        super().__init__(
            model=model,
            temperature=temperature,
            n=n,
            best_of=best_of,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            top_p=top_p,
            top_k=top_k,
            use_beam_search=use_beam_search,
            stop=stop,
            ignore_eos=ignore_eos,
            max_new_tokens=max_new_tokens,
            logprobs=logprobs,
            dtype=dtype,
            download_dir=download_dir,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            vllm_kwargs=vllm_kwargs,
            api_url=api_url,
            callback_manager=callback_manager,
            output_parser=output_parser,
        )

    @classmethod
    def class_name(cls) -> str:
        return "VllmServer"

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> List[CompletionResponse]:
        kwargs = kwargs if kwargs else {}
        params = {**self._model_kwargs, **kwargs}

        from vllm import SamplingParams

        # build sampling parameters
        sampling_params = SamplingParams(**params).__dict__
        sampling_params["prompt"] = prompt
        response = post_http_request(self.api_url, sampling_params, stream=False)
        output = get_response(response)

        return CompletionResponse(text=output[0])

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        kwargs = kwargs if kwargs else {}
        params = {**self._model_kwargs, **kwargs}

        from vllm import SamplingParams

        # build sampling parameters
        sampling_params = SamplingParams(**params).__dict__
        sampling_params["prompt"] = prompt
        response = post_http_request(self.api_url, sampling_params, stream=True)

        def gen() -> CompletionResponseGen:
            for chunk in response.iter_lines(
                chunk_size=8192, decode_unicode=False, delimiter=b"\0"
            ):
                if chunk:
                    data = json.loads(chunk.decode("utf-8"))

                    yield CompletionResponse(text=data["text"][0])

        return gen()

    @llm_completion_callback()
    async def acomplete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        kwargs = kwargs if kwargs else {}
        return self.complete(prompt, **kwargs)

    @llm_completion_callback()
    async def astream_complete(
        self, prompt: str, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        kwargs = kwargs if kwargs else {}
        params = {**self._model_kwargs, **kwargs}

        from vllm import SamplingParams

        # build sampling parameters
        sampling_params = SamplingParams(**params).__dict__
        sampling_params["prompt"] = prompt

        async def gen() -> CompletionResponseAsyncGen:
            for message in self.stream_complete(prompt, **kwargs):
                yield message

        return gen()

    @llm_chat_callback()
    def stream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        prompt = self.messages_to_prompt(messages)
        completion_response = self.stream_complete(prompt, **kwargs)
        return stream_completion_response_to_chat_response(completion_response)

    @llm_chat_callback()
    async def astream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        return self.stream_chat(messages, **kwargs)

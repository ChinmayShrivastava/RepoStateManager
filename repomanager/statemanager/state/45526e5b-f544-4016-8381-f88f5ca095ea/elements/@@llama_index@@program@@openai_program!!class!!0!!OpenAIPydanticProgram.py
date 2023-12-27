class OpenAIPydanticProgram(BaseLLMFunctionProgram[LLM]):
    """
    An OpenAI-based function that returns a pydantic model.

    Note: this interface is not yet stable.
    """

    def __init__(
        self,
        output_cls: Type[Model],
        llm: LLM,
        prompt: BasePromptTemplate,
        tool_choice: Union[str, Dict[str, Any]],
        allow_multiple: bool = False,
        verbose: bool = False,
    ) -> None:
        """Init params."""
        self._output_cls = output_cls
        self._llm = llm
        self._prompt = prompt
        self._verbose = verbose
        self._allow_multiple = allow_multiple
        self._tool_choice = tool_choice

    @classmethod
    def from_defaults(
        cls,
        output_cls: Type[Model],
        prompt_template_str: Optional[str] = None,
        prompt: Optional[PromptTemplate] = None,
        llm: Optional[LLM] = None,
        verbose: bool = False,
        allow_multiple: bool = False,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> "OpenAIPydanticProgram":
        llm = llm or OpenAI(model="gpt-3.5-turbo-0613")

        if not isinstance(llm, OpenAI):
            raise ValueError(
                "OpenAIPydanticProgram only supports OpenAI LLMs. " f"Got: {type(llm)}"
            )

        if not llm.metadata.is_function_calling_model:
            raise ValueError(
                f"Model name {llm.metadata.model_name} does not support "
                "function calling API. "
            )

        if prompt is None and prompt_template_str is None:
            raise ValueError("Must provide either prompt or prompt_template_str.")
        if prompt is not None and prompt_template_str is not None:
            raise ValueError("Must provide either prompt or prompt_template_str.")
        if prompt_template_str is not None:
            prompt = PromptTemplate(prompt_template_str)

        tool_choice = tool_choice or _default_tool_choice(output_cls, allow_multiple)

        return cls(
            output_cls=output_cls,
            llm=llm,
            prompt=cast(PromptTemplate, prompt),
            tool_choice=tool_choice,
            allow_multiple=allow_multiple,
            verbose=verbose,
        )

    @property
    def output_cls(self) -> Type[Model]:
        return self._output_cls

    @property
    def prompt(self) -> BasePromptTemplate:
        return self._prompt

    @prompt.setter
    def prompt(self, prompt: BasePromptTemplate) -> None:
        self._prompt = prompt

    def __call__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Union[Model, List[Model]]:
        openai_fn_spec = to_openai_tool(self._output_cls)

        messages = self._prompt.format_messages(llm=self._llm, **kwargs)

        chat_response = self._llm.chat(
            messages=messages,
            tools=[openai_fn_spec],
            tool_choice=self._tool_choice,
        )
        message = chat_response.message
        if "tool_calls" not in message.additional_kwargs:
            raise ValueError(
                "Expected tool_calls in ai_message.additional_kwargs, "
                "but none found."
            )

        tool_calls = message.additional_kwargs["tool_calls"]
        return _parse_tool_calls(
            tool_calls,
            output_cls=self.output_cls,
            allow_multiple=self._allow_multiple,
            verbose=self._verbose,
        )

    async def acall(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Union[Model, List[Model]]:
        openai_fn_spec = to_openai_tool(self._output_cls)

        messages = self._prompt.format_messages(llm=self._llm, **kwargs)

        chat_response = await self._llm.achat(
            messages=messages,
            tools=[openai_fn_spec],
            tool_choice=self._tool_choice,
        )
        message = chat_response.message
        if "tool_calls" not in message.additional_kwargs:
            raise ValueError(
                "Expected function call in ai_message.additional_kwargs, "
                "but none found."
            )

        tool_calls = message.additional_kwargs["tool_calls"]
        return _parse_tool_calls(
            tool_calls,
            output_cls=self.output_cls,
            allow_multiple=self._allow_multiple,
            verbose=self._verbose,
        )

    def stream_list(self, *args: Any, **kwargs: Any) -> Generator[Model, None, None]:
        """Streams a list of objects."""
        messages = self._prompt.format_messages(llm=self._llm, **kwargs)

        list_output_cls = create_list_model(self._output_cls)
        openai_fn_spec = to_openai_tool(list_output_cls)

        chat_response_gen = self._llm.stream_chat(
            messages=messages,
            tools=[openai_fn_spec],
            tool_choice=_default_tool_choice(list_output_cls),
        )
        # extract function call arguments
        # obj_start_idx finds start position (before a new "{" in JSON)
        obj_start_idx: int = -1  # NOTE: uninitialized
        for stream_resp in chat_response_gen:
            kwargs = stream_resp.message.additional_kwargs
            tool_calls = kwargs["tool_calls"]
            if len(tool_calls) == 0:
                continue

            # NOTE: right now assume only one tool call
            # TODO: handle parallel tool calls in streaming setting
            fn_args = kwargs["tool_calls"][0].function.arguments

            # this is inspired by `get_object` from `MultiTaskBase` in
            # the openai_function_call repo

            if fn_args.find("[") != -1:
                if obj_start_idx == -1:
                    obj_start_idx = fn_args.find("[") + 1
            else:
                # keep going until we find the start position
                continue

            new_obj_json_str, obj_start_idx = _get_json_str(fn_args, obj_start_idx)
            if new_obj_json_str is not None:
                obj_json_str = new_obj_json_str
                obj = self._output_cls.parse_raw(obj_json_str)
                if self._verbose:
                    print(f"Extracted object: {obj.json()}")
                yield obj

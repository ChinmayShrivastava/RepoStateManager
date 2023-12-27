class BaseOpenAIAgent(BaseAgent):
    def __init__(
        self,
        llm: OpenAI,
        memory: BaseMemory,
        prefix_messages: List[ChatMessage],
        verbose: bool,
        max_function_calls: int,
        callback_manager: Optional[CallbackManager],
    ):
        self._llm = llm
        self._verbose = verbose
        self._max_function_calls = max_function_calls
        self.prefix_messages = prefix_messages
        self.memory = memory
        self.callback_manager = callback_manager or self._llm.callback_manager
        self.sources: List[ToolOutput] = []

    @property
    def chat_history(self) -> List[ChatMessage]:
        return self.memory.get_all()

    @property
    def all_messages(self) -> List[ChatMessage]:
        return self.prefix_messages + self.memory.get()

    @property
    def latest_function_call(self) -> Optional[dict]:
        return self.memory.get_all()[-1].additional_kwargs.get("function_call", None)

    @property
    def latest_tool_calls(self) -> Optional[List[OpenAIToolCall]]:
        return self.memory.get_all()[-1].additional_kwargs.get("tool_calls", None)

    def reset(self) -> None:
        self.memory.reset()

    @abstractmethod
    def get_tools(self, message: str) -> List[BaseTool]:
        """Get tools."""

    def _should_continue(
        self, tool_calls: Optional[List[OpenAIToolCall]], n_function_calls: int
    ) -> bool:
        if n_function_calls > self._max_function_calls:
            return False
        if not tool_calls:
            return False
        return True

    def init_chat(
        self, message: str, chat_history: Optional[List[ChatMessage]] = None
    ) -> Tuple[List[BaseTool], List[dict]]:
        if chat_history is not None:
            self.memory.set(chat_history)
        self.sources = []
        self.memory.put(ChatMessage(content=message, role=MessageRole.USER))
        tools = self.get_tools(message)
        openai_tools = [tool.metadata.to_openai_tool() for tool in tools]
        return tools, openai_tools

    def _process_message(self, chat_response: ChatResponse) -> AgentChatResponse:
        ai_message = chat_response.message
        self.memory.put(ai_message)
        return AgentChatResponse(response=str(ai_message.content), sources=self.sources)

    def _get_stream_ai_response(
        self, **llm_chat_kwargs: Any
    ) -> StreamingAgentChatResponse:
        chat_stream_response = StreamingAgentChatResponse(
            chat_stream=self._llm.stream_chat(**llm_chat_kwargs),
            sources=self.sources,
        )
        # Get the response in a separate thread so we can yield the response
        thread = Thread(
            target=chat_stream_response.write_response_to_history,
            args=(self.memory,),
        )
        thread.start()
        # Wait for the event to be set
        chat_stream_response._is_function_not_none_thread_event.wait()
        # If it is executing an openAI function, wait for the thread to finish
        if chat_stream_response._is_function:
            thread.join()

        # if it's false, return the answer (to stream)
        return chat_stream_response

    async def _get_async_stream_ai_response(
        self, **llm_chat_kwargs: Any
    ) -> StreamingAgentChatResponse:
        chat_stream_response = StreamingAgentChatResponse(
            achat_stream=await self._llm.astream_chat(**llm_chat_kwargs),
            sources=self.sources,
        )
        # create task to write chat response to history
        asyncio.create_task(
            chat_stream_response.awrite_response_to_history(self.memory)
        )
        # wait until openAI functions stop executing
        await chat_stream_response._is_function_false_event.wait()
        # return response stream
        return chat_stream_response

    def _call_function(self, tools: List[BaseTool], tool_call: OpenAIToolCall) -> None:
        function_call = tool_call.function
        # validations to get passed mypy
        assert function_call is not None
        assert function_call.name is not None
        assert function_call.arguments is not None

        with self.callback_manager.event(
            CBEventType.FUNCTION_CALL,
            payload={
                EventPayload.FUNCTION_CALL: function_call.arguments,
                EventPayload.TOOL: get_function_by_name(
                    tools, function_call.name
                ).metadata,
            },
        ) as event:
            function_message, tool_output = call_function(
                tools, tool_call, verbose=self._verbose
            )
            event.on_end(payload={EventPayload.FUNCTION_OUTPUT: str(tool_output)})
        self.sources.append(tool_output)
        self.memory.put(function_message)

    async def _acall_function(
        self, tools: List[BaseTool], tool_call: OpenAIToolCall
    ) -> None:
        function_call = tool_call.function
        # validations to get passed mypy
        assert function_call is not None
        assert function_call.name is not None
        assert function_call.arguments is not None

        with self.callback_manager.event(
            CBEventType.FUNCTION_CALL,
            payload={
                EventPayload.FUNCTION_CALL: function_call.arguments,
                EventPayload.TOOL: get_function_by_name(
                    tools, function_call.name
                ).metadata,
            },
        ) as event:
            function_message, tool_output = await acall_function(
                tools, tool_call, verbose=self._verbose
            )
            event.on_end(payload={EventPayload.FUNCTION_OUTPUT: str(tool_output)})
        self.sources.append(tool_output)
        self.memory.put(function_message)

    def _get_llm_chat_kwargs(
        self, openai_tools: List[dict], tool_choice: Union[str, dict] = "auto"
    ) -> Dict[str, Any]:
        llm_chat_kwargs: dict = {"messages": self.all_messages}
        if openai_tools:
            llm_chat_kwargs.update(
                tools=openai_tools, tool_choice=resolve_tool_choice(tool_choice)
            )
        return llm_chat_kwargs

    def _get_agent_response(
        self, mode: ChatResponseMode, **llm_chat_kwargs: Any
    ) -> AGENT_CHAT_RESPONSE_TYPE:
        if mode == ChatResponseMode.WAIT:
            chat_response: ChatResponse = self._llm.chat(**llm_chat_kwargs)
            return self._process_message(chat_response)
        elif mode == ChatResponseMode.STREAM:
            return self._get_stream_ai_response(**llm_chat_kwargs)
        else:
            raise NotImplementedError

    async def _get_async_agent_response(
        self, mode: ChatResponseMode, **llm_chat_kwargs: Any
    ) -> AGENT_CHAT_RESPONSE_TYPE:
        if mode == ChatResponseMode.WAIT:
            chat_response: ChatResponse = await self._llm.achat(**llm_chat_kwargs)
            return self._process_message(chat_response)
        elif mode == ChatResponseMode.STREAM:
            return await self._get_async_stream_ai_response(**llm_chat_kwargs)
        else:
            raise NotImplementedError

    def _chat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        tool_choice: Union[str, dict] = "auto",
        mode: ChatResponseMode = ChatResponseMode.WAIT,
    ) -> AGENT_CHAT_RESPONSE_TYPE:
        tools, openai_tools = self.init_chat(message, chat_history)
        n_function_calls = 0

        # Loop until no more function calls or max_function_calls is reached
        current_tool_choice = tool_choice
        ix = 0
        while True:
            ix += 1
            if self._verbose:
                print(f"STARTING TURN {ix}\n---------------\n")
            llm_chat_kwargs = self._get_llm_chat_kwargs(
                openai_tools, current_tool_choice
            )
            agent_chat_response = self._get_agent_response(mode=mode, **llm_chat_kwargs)
            if not self._should_continue(self.latest_tool_calls, n_function_calls):
                logger.debug("Break: should continue False")
                break
            # iterate through all the tool calls
            logger.debug(f"Continue to tool calls: {self.latest_tool_calls}")
            if self.latest_tool_calls is not None:
                for tool_call in self.latest_tool_calls:
                    # Some validation
                    if not isinstance(tool_call, get_args(OpenAIToolCall)):
                        raise ValueError("Invalid tool_call object")

                    if tool_call.type != "function":
                        raise ValueError("Invalid tool type. Unsupported by OpenAI")
                    # TODO: maybe execute this with multi-threading
                    self._call_function(tools, tool_call)
                    # change function call to the default value, if a custom function was given
                    # as an argument (none and auto are predefined by OpenAI)
                    if current_tool_choice not in ("auto", "none"):
                        current_tool_choice = "auto"
                    n_function_calls += 1

        return agent_chat_response

    async def _achat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        tool_choice: Union[str, dict] = "auto",
        mode: ChatResponseMode = ChatResponseMode.WAIT,
    ) -> AGENT_CHAT_RESPONSE_TYPE:
        tools, functions = self.init_chat(message, chat_history)
        n_function_calls = 0

        # Loop until no more function calls or max_function_calls is reached
        current_tool_choice = tool_choice
        ix = 0
        while True:
            ix += 1
            if self._verbose:
                print(f"STARTING TURN {ix}\n---------------\n")
            llm_chat_kwargs = self._get_llm_chat_kwargs(functions, current_tool_choice)
            agent_chat_response = await self._get_async_agent_response(
                mode=mode, **llm_chat_kwargs
            )
            if not self._should_continue(self.latest_tool_calls, n_function_calls):
                break
            # iterate through all the tool calls
            if self.latest_tool_calls is not None:
                for tool_call in self.latest_tool_calls:
                    # Some validation
                    if not isinstance(tool_call, get_args(OpenAIToolCall)):
                        raise ValueError("Invalid tool_call object")

                    if tool_call.type != "function":
                        raise ValueError("Invalid tool type. Unsupported by OpenAI")

                    # TODO: maybe execute this with multi-threading
                    await self._acall_function(tools, tool_call)
                    # change function call to the default value, if a custom function was given
                    # as an argument (none and auto are predefined by OpenAI)
                    if current_tool_choice not in ("auto", "none"):
                        current_tool_choice = "auto"
                    n_function_calls += 1

        return agent_chat_response

    @trace_method("chat")
    def chat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        tool_choice: Union[str, dict] = "auto",
    ) -> AgentChatResponse:
        with self.callback_manager.event(
            CBEventType.AGENT_STEP,
            payload={EventPayload.MESSAGES: [message]},
        ) as e:
            chat_response = self._chat(
                message, chat_history, tool_choice, mode=ChatResponseMode.WAIT
            )
            assert isinstance(chat_response, AgentChatResponse)
            e.on_end(payload={EventPayload.RESPONSE: chat_response})
        return chat_response

    @trace_method("chat")
    async def achat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        tool_choice: Union[str, dict] = "auto",
    ) -> AgentChatResponse:
        with self.callback_manager.event(
            CBEventType.AGENT_STEP,
            payload={EventPayload.MESSAGES: [message]},
        ) as e:
            chat_response = await self._achat(
                message, chat_history, tool_choice, mode=ChatResponseMode.WAIT
            )
            assert isinstance(chat_response, AgentChatResponse)
            e.on_end(payload={EventPayload.RESPONSE: chat_response})
        return chat_response

    @trace_method("chat")
    def stream_chat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        tool_choice: Union[str, dict] = "auto",
    ) -> StreamingAgentChatResponse:
        with self.callback_manager.event(
            CBEventType.AGENT_STEP,
            payload={EventPayload.MESSAGES: [message]},
        ) as e:
            chat_response = self._chat(
                message, chat_history, tool_choice, mode=ChatResponseMode.STREAM
            )
            assert isinstance(chat_response, StreamingAgentChatResponse)
            e.on_end(payload={EventPayload.RESPONSE: chat_response})
        return chat_response

    @trace_method("chat")
    async def astream_chat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        tool_choice: Union[str, dict] = "auto",
    ) -> StreamingAgentChatResponse:
        with self.callback_manager.event(
            CBEventType.AGENT_STEP,
            payload={EventPayload.MESSAGES: [message]},
        ) as e:
            chat_response = await self._achat(
                message, chat_history, tool_choice, mode=ChatResponseMode.STREAM
            )
            assert isinstance(chat_response, StreamingAgentChatResponse)
            e.on_end(payload={EventPayload.RESPONSE: chat_response})
        return chat_response

class OpenAIAssistantAgent(BaseAgent):
    """OpenAIAssistant agent.

    Wrapper around OpenAI assistant API: https://platform.openai.com/docs/assistants/overview

    """

    def __init__(
        self,
        client: Any,
        assistant: Any,
        tools: Optional[List[BaseTool]],
        callback_manager: Optional[CallbackManager] = None,
        thread_id: Optional[str] = None,
        instructions_prefix: Optional[str] = None,
        run_retrieve_sleep_time: float = 0.1,
        file_dict: Dict[str, str] = {},
        verbose: bool = False,
    ) -> None:
        """Init params."""
        from openai import OpenAI
        from openai.types.beta.assistant import Assistant

        self._client = cast(OpenAI, client)
        self._assistant = cast(Assistant, assistant)
        self._tools = tools or []
        if thread_id is None:
            thread = self._client.beta.threads.create()
            thread_id = thread.id
        self._thread_id = thread_id
        self._instructions_prefix = instructions_prefix
        self._run_retrieve_sleep_time = run_retrieve_sleep_time
        self._verbose = verbose
        self.file_dict = file_dict

        self.callback_manager = callback_manager or CallbackManager([])

    @classmethod
    def from_new(
        cls,
        name: str,
        instructions: str,
        tools: Optional[List[BaseTool]] = None,
        openai_tools: Optional[List[Dict]] = None,
        thread_id: Optional[str] = None,
        model: str = "gpt-4-1106-preview",
        instructions_prefix: Optional[str] = None,
        run_retrieve_sleep_time: float = 0.1,
        files: Optional[List[str]] = None,
        callback_manager: Optional[CallbackManager] = None,
        verbose: bool = False,
        file_ids: Optional[List[str]] = None,
        api_key: Optional[str] = None,
    ) -> "OpenAIAssistantAgent":
        """From new assistant.

        Args:
            name: name of assistant
            instructions: instructions for assistant
            tools: list of tools
            openai_tools: list of openai tools
            thread_id: thread id
            model: model
            run_retrieve_sleep_time: run retrieve sleep time
            files: files
            instructions_prefix: instructions prefix
            callback_manager: callback manager
            verbose: verbose
            file_ids: list of file ids
            api_key: OpenAI API key

        """
        from openai import OpenAI

        # this is the set of openai tools
        # not to be confused with the tools we pass in for function calling
        openai_tools = openai_tools or []
        tools = tools or []
        tool_fns = [t.metadata.to_openai_tool() for t in tools]
        all_openai_tools = openai_tools + tool_fns

        # initialize client
        client = OpenAI(api_key=api_key)

        # process files
        files = files or []
        file_ids = file_ids or []

        file_dict = _process_files(client, files)
        all_file_ids = list(file_dict.keys()) + file_ids

        # TODO: openai's typing is a bit sus
        all_openai_tools = cast(List[Any], all_openai_tools)
        assistant = client.beta.assistants.create(
            name=name,
            instructions=instructions,
            tools=cast(List[Any], all_openai_tools),
            model=model,
            file_ids=all_file_ids + file_ids,
        )
        return cls(
            client,
            assistant,
            tools,
            callback_manager=callback_manager,
            thread_id=thread_id,
            instructions_prefix=instructions_prefix,
            file_dict=file_dict,
            run_retrieve_sleep_time=run_retrieve_sleep_time,
            verbose=verbose,
        )

    @classmethod
    def from_existing(
        cls,
        assistant_id: str,
        tools: Optional[List[BaseTool]] = None,
        thread_id: Optional[str] = None,
        instructions_prefix: Optional[str] = None,
        run_retrieve_sleep_time: float = 0.1,
        callback_manager: Optional[CallbackManager] = None,
        api_key: Optional[str] = None,
        verbose: bool = False,
    ) -> "OpenAIAssistantAgent":
        """From existing assistant id.

        Args:
            assistant_id: id of assistant
            tools: list of BaseTools Assistant can use
            thread_id: thread id
            run_retrieve_sleep_time: run retrieve sleep time
            instructions_prefix: instructions prefix
            callback_manager: callback manager
            api_key: OpenAI API key
            verbose: verbose

        """
        from openai import OpenAI

        # initialize client
        client = OpenAI(api_key=api_key)

        # get assistant
        assistant = client.beta.assistants.retrieve(assistant_id)
        # assistant.tools is incompatible with BaseTools so have to pass from params

        return cls(
            client,
            assistant,
            tools=tools,
            callback_manager=callback_manager,
            thread_id=thread_id,
            instructions_prefix=instructions_prefix,
            run_retrieve_sleep_time=run_retrieve_sleep_time,
            verbose=verbose,
        )

    @property
    def assistant(self) -> Any:
        """Get assistant."""
        return self._assistant

    @property
    def client(self) -> Any:
        """Get client."""
        return self._client

    @property
    def thread_id(self) -> str:
        """Get thread id."""
        return self._thread_id

    @property
    def files_dict(self) -> Dict[str, str]:
        """Get files dict."""
        return self.file_dict

    @property
    def chat_history(self) -> List[ChatMessage]:
        raw_messages = self._client.beta.threads.messages.list(
            thread_id=self._thread_id, order="asc"
        )
        return from_openai_thread_messages(list(raw_messages))

    def reset(self) -> None:
        """Delete and create a new thread."""
        self._client.beta.threads.delete(self._thread_id)
        thread = self._client.beta.threads.create()
        thread_id = thread.id
        self._thread_id = thread_id

    def get_tools(self, message: str) -> List[BaseTool]:
        """Get tools."""
        return self._tools

    def upload_files(self, files: List[str]) -> Dict[str, Any]:
        """Upload files."""
        return _process_files(self._client, files)

    def add_message(self, message: str, file_ids: Optional[List[str]] = None) -> Any:
        """Add message to assistant."""
        file_ids = file_ids or []
        return self._client.beta.threads.messages.create(
            thread_id=self._thread_id,
            role="user",
            content=message,
            file_ids=file_ids,
        )

    def _run_function_calling(self, run: Any) -> List[ToolOutput]:
        """Run function calling."""
        tool_calls = run.required_action.submit_tool_outputs.tool_calls
        tool_output_dicts = []
        tool_output_objs: List[ToolOutput] = []
        for tool_call in tool_calls:
            fn_obj = tool_call.function
            _, tool_output = call_function(self._tools, fn_obj, verbose=self._verbose)
            tool_output_dicts.append(
                {"tool_call_id": tool_call.id, "output": str(tool_output)}
            )
            tool_output_objs.append(tool_output)

        # submit tool outputs
        # TODO: openai's typing is a bit sus
        self._client.beta.threads.runs.submit_tool_outputs(
            thread_id=self._thread_id,
            run_id=run.id,
            tool_outputs=cast(List[Any], tool_output_dicts),
        )
        return tool_output_objs

    async def _arun_function_calling(self, run: Any) -> List[ToolOutput]:
        """Run function calling."""
        tool_calls = run.required_action.submit_tool_outputs.tool_calls
        tool_output_dicts = []
        tool_output_objs: List[ToolOutput] = []
        for tool_call in tool_calls:
            fn_obj = tool_call.function
            _, tool_output = await acall_function(
                self._tools, fn_obj, verbose=self._verbose
            )
            tool_output_dicts.append(
                {"tool_call_id": tool_call.id, "output": str(tool_output)}
            )
            tool_output_objs.append(tool_output)

        # submit tool outputs
        self._client.beta.threads.runs.submit_tool_outputs(
            thread_id=self._thread_id,
            run_id=run.id,
            tool_outputs=cast(List[Any], tool_output_dicts),
        )
        return tool_output_objs

    def run_assistant(
        self, instructions_prefix: Optional[str] = None
    ) -> Tuple[Any, Dict]:
        """Run assistant."""
        instructions_prefix = instructions_prefix or self._instructions_prefix
        run = self._client.beta.threads.runs.create(
            thread_id=self._thread_id,
            assistant_id=self._assistant.id,
            instructions=instructions_prefix,
        )
        from openai.types.beta.threads import Run

        run = cast(Run, run)

        sources = []

        while run.status in ["queued", "in_progress", "requires_action"]:
            run = self._client.beta.threads.runs.retrieve(
                thread_id=self._thread_id, run_id=run.id
            )
            if run.status == "requires_action":
                cur_tool_outputs = self._run_function_calling(run)
                sources.extend(cur_tool_outputs)

            time.sleep(self._run_retrieve_sleep_time)
        if run.status == "failed":
            raise ValueError(
                f"Run failed with status {run.status}.\n" f"Error: {run.last_error}"
            )
        return run, {"sources": sources}

    async def arun_assistant(
        self, instructions_prefix: Optional[str] = None
    ) -> Tuple[Any, Dict]:
        """Run assistant."""
        instructions_prefix = instructions_prefix or self._instructions_prefix
        run = self._client.beta.threads.runs.create(
            thread_id=self._thread_id,
            assistant_id=self._assistant.id,
            instructions=instructions_prefix,
        )
        from openai.types.beta.threads import Run

        run = cast(Run, run)

        sources = []

        while run.status in ["queued", "in_progress", "requires_action"]:
            run = self._client.beta.threads.runs.retrieve(
                thread_id=self._thread_id, run_id=run.id
            )
            if run.status == "requires_action":
                cur_tool_outputs = await self._arun_function_calling(run)
                sources.extend(cur_tool_outputs)

            await asyncio.sleep(self._run_retrieve_sleep_time)
        if run.status == "failed":
            raise ValueError(
                f"Run failed with status {run.status}.\n" f"Error: {run.last_error}"
            )
        return run, {"sources": sources}

    @property
    def latest_message(self) -> ChatMessage:
        """Get latest message."""
        raw_messages = self._client.beta.threads.messages.list(
            thread_id=self._thread_id, order="desc"
        )
        messages = from_openai_thread_messages(list(raw_messages))
        return messages[0]

    def _chat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        function_call: Union[str, dict] = "auto",
        mode: ChatResponseMode = ChatResponseMode.WAIT,
    ) -> AGENT_CHAT_RESPONSE_TYPE:
        """Main chat interface."""
        # TODO: since chat interface doesn't expose additional kwargs
        # we can't pass in file_ids per message
        added_message_obj = self.add_message(message)
        run, metadata = self.run_assistant(
            instructions_prefix=self._instructions_prefix,
        )
        latest_message = self.latest_message
        # get most recent message content
        return AgentChatResponse(
            response=str(latest_message.content),
            sources=metadata["sources"],
        )

    async def _achat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        function_call: Union[str, dict] = "auto",
        mode: ChatResponseMode = ChatResponseMode.WAIT,
    ) -> AGENT_CHAT_RESPONSE_TYPE:
        """Asynchronous main chat interface."""
        self.add_message(message)
        run, metadata = await self.arun_assistant(
            instructions_prefix=self._instructions_prefix,
        )
        latest_message = self.latest_message
        # get most recent message content
        return AgentChatResponse(
            response=str(latest_message.content),
            sources=metadata["sources"],
        )

    @trace_method("chat")
    def chat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        function_call: Union[str, dict] = "auto",
    ) -> AgentChatResponse:
        with self.callback_manager.event(
            CBEventType.AGENT_STEP,
            payload={EventPayload.MESSAGES: [message]},
        ) as e:
            chat_response = self._chat(
                message, chat_history, function_call, mode=ChatResponseMode.WAIT
            )
            assert isinstance(chat_response, AgentChatResponse)
            e.on_end(payload={EventPayload.RESPONSE: chat_response})
        return chat_response

    @trace_method("chat")
    async def achat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        function_call: Union[str, dict] = "auto",
    ) -> AgentChatResponse:
        with self.callback_manager.event(
            CBEventType.AGENT_STEP,
            payload={EventPayload.MESSAGES: [message]},
        ) as e:
            chat_response = await self._achat(
                message, chat_history, function_call, mode=ChatResponseMode.WAIT
            )
            assert isinstance(chat_response, AgentChatResponse)
            e.on_end(payload={EventPayload.RESPONSE: chat_response})
        return chat_response

    @trace_method("chat")
    def stream_chat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        function_call: Union[str, dict] = "auto",
    ) -> StreamingAgentChatResponse:
        raise NotImplementedError("stream_chat not implemented")

    @trace_method("chat")
    async def astream_chat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        function_call: Union[str, dict] = "auto",
    ) -> StreamingAgentChatResponse:
        raise NotImplementedError("astream_chat not implemented")

class StreamingAgentChatResponse:
    """Streaming chat response to user and writing to chat history."""

    response: str = ""
    sources: List[ToolOutput] = field(default_factory=list)
    chat_stream: Optional[ChatResponseGen] = None
    achat_stream: Optional[ChatResponseAsyncGen] = None
    source_nodes: List[NodeWithScore] = field(default_factory=list)
    _unformatted_response: str = ""
    _queue: queue.Queue = field(default_factory=queue.Queue)
    _aqueue: asyncio.Queue = field(default_factory=asyncio.Queue)
    # flag when chat message is a function call
    _is_function: Optional[bool] = None
    # flag when processing done
    _is_done = False
    # signal when a new item is added to the queue
    _new_item_event: asyncio.Event = field(default_factory=asyncio.Event)
    # NOTE: async code uses two events rather than one since it yields
    # control when waiting for queue item
    # signal when the OpenAI functions stop executing
    _is_function_false_event: asyncio.Event = field(default_factory=asyncio.Event)
    # signal when an OpenAI function is being executed
    _is_function_not_none_thread_event: Event = field(default_factory=Event)

    def __post_init__(self) -> None:
        if self.sources and not self.source_nodes:
            for tool_output in self.sources:
                if isinstance(tool_output.raw_output, (Response, StreamingResponse)):
                    self.source_nodes.extend(tool_output.raw_output.source_nodes)

    def __str__(self) -> str:
        if self._is_done and not self._queue.empty() and not self._is_function:
            while self._queue.queue:
                delta = self._queue.queue.popleft()
                self._unformatted_response += delta
            self.response = self._unformatted_response.strip()
        return self.response

    def put_in_queue(self, delta: Optional[str]) -> None:
        self._queue.put_nowait(delta)
        self._is_function_not_none_thread_event.set()

    def aput_in_queue(self, delta: Optional[str]) -> None:
        self._aqueue.put_nowait(delta)
        self._new_item_event.set()

    def write_response_to_history(self, memory: BaseMemory) -> None:
        if self.chat_stream is None:
            raise ValueError(
                "chat_stream is None. Cannot write to history without chat_stream."
            )

        # try/except to prevent hanging on error
        try:
            final_text = ""
            for chat in self.chat_stream:
                self._is_function = is_function(chat.message)
                self.put_in_queue(chat.delta)
                final_text += chat.delta or ""
            if self._is_function is not None:  # if loop has gone through iteration
                # NOTE: this is to handle the special case where we consume some of the
                # chat stream, but not all of it (e.g. in react agent)
                chat.message.content = final_text.strip()  # final message
                memory.put(chat.message)
        except Exception as e:
            logger.warning(f"Encountered exception writing response to history: {e}")

        self._is_done = True

    async def awrite_response_to_history(
        self,
        memory: BaseMemory,
    ) -> None:
        if self.achat_stream is None:
            raise ValueError(
                "achat_stream is None. Cannot asynchronously write to "
                "history without achat_stream."
            )

        # try/except to prevent hanging on error
        try:
            final_text = ""
            async for chat in self.achat_stream:
                self._is_function = is_function(chat.message)
                self.aput_in_queue(chat.delta)
                final_text += chat.delta or ""
                if self._is_function is False:
                    self._is_function_false_event.set()
            if self._is_function is not None:  # if loop has gone through iteration
                # NOTE: this is to handle the special case where we consume some of the
                # chat stream, but not all of it (e.g. in react agent)
                chat.message.content = final_text.strip()  # final message
                memory.put(chat.message)
        except Exception as e:
            logger.warning(f"Encountered exception writing response to history: {e}")
        self._is_done = True

        # These act as is_done events for any consumers waiting
        self._is_function_false_event.set()
        self._new_item_event.set()

    @property
    def response_gen(self) -> Generator[str, None, None]:
        while not self._is_done or not self._queue.empty():
            try:
                delta = self._queue.get(block=False)
                self._unformatted_response += delta
                yield delta
            except queue.Empty:
                # Queue is empty, but we're not done yet
                continue
        self.response = self._unformatted_response.strip()

    async def async_response_gen(self) -> AsyncGenerator[str, None]:
        while not self._is_done or not self._aqueue.empty():
            if not self._aqueue.empty():
                delta = self._aqueue.get_nowait()
                self._unformatted_response += delta
                yield delta
            else:
                await self._new_item_event.wait()  # Wait until a new item is added
                self._new_item_event.clear()  # Clear the event for the next wait
        self.response = self._unformatted_response.strip()

    def print_response_stream(self) -> None:
        for token in self.response_gen:
            print(token, end="", flush=True)

    async def aprint_response_stream(self) -> None:
        async for token in self.async_response_gen():
            print(token, end="", flush=True)

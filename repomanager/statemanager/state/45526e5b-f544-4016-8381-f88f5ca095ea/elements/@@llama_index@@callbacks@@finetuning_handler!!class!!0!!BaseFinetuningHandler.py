class BaseFinetuningHandler(BaseCallbackHandler):
    """
    Callback handler for finetuning.

    This handler will collect all messages
    sent to the LLM, along with their responses.
    It also defines a `get_finetuning_events` endpoint as well as a
    `save_finetuning_events` endpoint.

    """

    def __init__(self) -> None:
        """Initialize the base callback handler."""
        super().__init__(
            event_starts_to_ignore=[],
            event_ends_to_ignore=[],
        )
        self._finetuning_events: Dict[str, List[Any]] = {}
        self._function_calls: Dict[str, List[Any]] = {}

    def on_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        parent_id: str = "",
        **kwargs: Any,
    ) -> str:
        """Run when an event starts and return id of event."""
        from llama_index.llms.types import ChatMessage, MessageRole

        if event_type == CBEventType.LLM:
            cur_messages = []
            if payload and EventPayload.PROMPT in payload:
                message = ChatMessage(
                    role=MessageRole.USER, text=str(payload[EventPayload.PROMPT])
                )
                cur_messages = [message]
            elif payload and EventPayload.MESSAGES in payload:
                cur_messages = payload[EventPayload.MESSAGES]

            if len(cur_messages) > 0:
                if event_id in self._finetuning_events:
                    self._finetuning_events[event_id].extend(cur_messages)
                else:
                    self._finetuning_events[event_id] = cur_messages

            # if functions exists, add that
            if payload and EventPayload.ADDITIONAL_KWARGS in payload:
                kwargs_dict = payload[EventPayload.ADDITIONAL_KWARGS]
                if "functions" in kwargs_dict:
                    self._function_calls[event_id] = kwargs_dict["functions"]
        return event_id

    def on_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
        """Run when an event ends."""
        from llama_index.llms.types import ChatMessage, MessageRole

        if (
            event_type == CBEventType.LLM
            and event_id in self._finetuning_events
            and payload is not None
        ):
            if isinstance(payload[EventPayload.RESPONSE], str):
                response = ChatMessage(
                    role=MessageRole.ASSISTANT, text=str(payload[EventPayload.RESPONSE])
                )
            else:
                response = payload[EventPayload.RESPONSE].message

            self._finetuning_events[event_id].append(response)

    @abstractmethod
    def get_finetuning_events(self) -> Dict[str, Dict[str, Any]]:
        """Get finetuning events."""

    @abstractmethod
    def save_finetuning_events(self, path: str) -> None:
        """Save the finetuning events to a file."""

    def start_trace(self, trace_id: Optional[str] = None) -> None:
        """Run when an overall trace is launched."""

    def end_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        """Run when an overall trace is exited."""

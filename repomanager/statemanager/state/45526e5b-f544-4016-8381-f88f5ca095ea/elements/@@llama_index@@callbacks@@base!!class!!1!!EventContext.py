class EventContext:
    """
    Simple wrapper to call callbacks on event starts and ends
    with an event type and id.
    """

    def __init__(
        self,
        callback_manager: CallbackManager,
        event_type: CBEventType,
        event_id: Optional[str] = None,
    ):
        self._callback_manager = callback_manager
        self._event_type = event_type
        self._event_id = event_id or str(uuid.uuid4())
        self.started = False
        self.finished = False

    def on_start(self, payload: Optional[Dict[str, Any]] = None, **kwargs: Any) -> None:
        if not self.started:
            self.started = True
            self._callback_manager.on_event_start(
                self._event_type, payload=payload, event_id=self._event_id, **kwargs
            )
        else:
            logger.warning(
                f"Event {self._event_type!s}: {self._event_id} already started!"
            )

    def on_end(self, payload: Optional[Dict[str, Any]] = None, **kwargs: Any) -> None:
        if not self.finished:
            self.finished = True
            self._callback_manager.on_event_end(
                self._event_type, payload=payload, event_id=self._event_id, **kwargs
            )

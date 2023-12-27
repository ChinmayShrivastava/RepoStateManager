class OpenInferenceCallbackHandler(BaseCallbackHandler):
    """Callback handler for storing generation data in OpenInference format.
    OpenInference is an open standard for capturing and storing AI model
    inferences. It enables production LLMapp servers to seamlessly integrate
    with LLM observability solutions such as Arize and Phoenix.

    For more information on the specification, see
    https://github.com/Arize-ai/open-inference-spec
    """

    def __init__(
        self,
        callback: Optional[Callable[[List[QueryData], List[NodeData]], None]] = None,
    ) -> None:
        """Initializes the OpenInferenceCallbackHandler.

        Args:
            callback (Optional[Callable[[List[QueryData], List[NodeData]], None]], optional): A
            callback function that will be called when a query trace is
            completed, often used for logging or persisting query data.
        """
        super().__init__(event_starts_to_ignore=[], event_ends_to_ignore=[])
        self._callback = callback
        self._trace_data = TraceData()
        self._query_data_buffer: List[QueryData] = []
        self._node_data_buffer: List[NodeData] = []

    def start_trace(self, trace_id: Optional[str] = None) -> None:
        if trace_id == "query":
            self._trace_data = TraceData()
            self._trace_data.query_data.timestamp = datetime.now().isoformat()
            self._trace_data.query_data.id = _generate_random_id()

    def end_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        if trace_id == "query":
            self._query_data_buffer.append(self._trace_data.query_data)
            self._node_data_buffer.extend(self._trace_data.node_datas)
            self._trace_data = TraceData()
            if self._callback is not None:
                self._callback(self._query_data_buffer, self._node_data_buffer)

    def on_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        parent_id: str = "",
        **kwargs: Any,
    ) -> str:
        if payload is not None:
            if event_type is CBEventType.QUERY:
                query_text = payload[EventPayload.QUERY_STR]
                self._trace_data.query_data.query_text = query_text
        return event_id

    def on_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
        if payload is None:
            return
        if event_type is CBEventType.RETRIEVE:
            for node_with_score in payload[EventPayload.NODES]:
                node = node_with_score.node
                score = node_with_score.score
                self._trace_data.query_data.node_ids.append(node.hash)
                self._trace_data.query_data.scores.append(score)
                self._trace_data.node_datas.append(
                    NodeData(
                        id=node.hash,
                        node_text=node.text,
                    )
                )
        elif event_type is CBEventType.LLM:
            self._trace_data.query_data.response_text = str(
                payload.get(EventPayload.RESPONSE, "")
            ) or str(payload.get(EventPayload.COMPLETION, ""))
        elif event_type is CBEventType.EMBEDDING:
            self._trace_data.query_data.query_embedding = payload[
                EventPayload.EMBEDDINGS
            ][0]

    def flush_query_data_buffer(self) -> List[QueryData]:
        """Clears the query data buffer and returns the data.

        Returns:
            List[QueryData]: The query data.
        """
        query_data_buffer = self._query_data_buffer
        self._query_data_buffer = []
        return query_data_buffer

    def flush_node_data_buffer(self) -> List[NodeData]:
        """Clears the node data buffer and returns the data.

        Returns:
            List[NodeData]: The node data.
        """
        node_data_buffer = self._node_data_buffer
        self._node_data_buffer = []
        return node_data_buffer

class MockStreamChatLLM(MockLLM):
    _i: int = PrivateAttr()
    _responses: List[ChatMessage] = PrivateAttr()

    def __init__(self, responses: List[ChatMessage]) -> None:
        self._i = 0  # call counter, determines which response to return
        self._responses = responses  # list of responses to return

        super().__init__()

    def stream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        del messages  # unused
        full_message = self._responses[self._i]
        self._i += 1

        role = full_message.role
        full_text = full_message.content or ""

        text_so_far = ""
        # create mock stream
        mock_stream = re.split(r"(\s+)", full_text)
        for token in mock_stream:
            text_so_far += token
            message = ChatMessage(
                content=text_so_far,
                role=role,
            )
            yield ChatResponse(
                message=message,
                delta=token,
            )

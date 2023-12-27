def test_chat(chat_history: Sequence[ChatMessage]) -> None:
    dummy = MockXinference("uid", "endpoint")
    response = dummy.chat(chat_history)
    assert isinstance(response, ChatResponse)
    assert response.delta is None
    assert response.message.role == MessageRole.ASSISTANT
    assert response.message.content == "test_response"

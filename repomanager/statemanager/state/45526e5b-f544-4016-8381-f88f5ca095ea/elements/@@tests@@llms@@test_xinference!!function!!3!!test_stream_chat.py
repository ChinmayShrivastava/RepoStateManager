def test_stream_chat(chat_history: Sequence[ChatMessage]) -> None:
    dummy = MockXinference("uid", "endpoint")
    response_gen = dummy.stream_chat(chat_history)
    total_text = ""
    for i, res in enumerate(response_gen):
        assert i < len(mock_chat_stream)
        assert isinstance(res, ChatResponse)
        assert isinstance(mock_chat_stream[i]["choices"], List)
        assert isinstance(mock_chat_stream[i]["choices"][0], Dict)
        assert isinstance(mock_chat_stream[i]["choices"][0]["delta"], Dict)
        assert res.delta == mock_chat_stream[i]["choices"][0]["delta"].get(
            "content", ""
        )
        assert res.message.role == MessageRole.ASSISTANT

        total_text += mock_chat_stream[i]["choices"][0]["delta"].get("content", "")
        assert total_text == res.message.content

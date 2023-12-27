def test_stream_complete() -> None:
    message = "test_input"
    dummy = MockXinference("uid", "endpoint")
    response_gen = dummy.stream_complete(message)
    total_text = ""
    for i, res in enumerate(response_gen):
        assert i < len(mock_chat_stream)
        assert isinstance(res, CompletionResponse)
        assert res.delta == mock_chat_stream[i]["choices"][0]["delta"].get(
            "content", ""
        )

        total_text += mock_chat_stream[i]["choices"][0]["delta"].get("content", "")
        assert total_text == res.text

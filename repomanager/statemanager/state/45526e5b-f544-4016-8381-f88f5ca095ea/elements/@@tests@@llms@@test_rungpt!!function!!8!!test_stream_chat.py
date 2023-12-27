def test_stream_chat(chat_history: List[ChatMessage]) -> None:
    mock_events = [
        MagicMock(data=event_data) for event_data in mock_chat_completion_stream()
    ]
    mock_event_iterator = iter(mock_events)

    with patch("requests.post"), patch("sseclient.SSEClient") as mock_sseclient:
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        type(mock_response).status_code = 200
        mock_sseclient.return_value.events.return_value = mock_event_iterator

        dummy = RunGptLLM()
        response_gen = dummy.stream_chat(chat_history)
        responses = list(response_gen)
        assert responses[-1].message.content == " This is test."
        assert responses[-1].message.role == "assistant"

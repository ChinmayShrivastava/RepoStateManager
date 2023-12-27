def test_chat(chat_history: List[ChatMessage]) -> None:
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_chat_completion()
        dummy = RunGptLLM()
        response = dummy.chat(chat_history)
        assert response.message.content == "This is an indeed test."
        assert response.message.role == "assistant"

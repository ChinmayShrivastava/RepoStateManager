def test_complete() -> None:
    dummy = RunGptLLM()
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_completion()
        response = dummy.complete("mock prompt")
        assert response.text == "This is an indeed test."

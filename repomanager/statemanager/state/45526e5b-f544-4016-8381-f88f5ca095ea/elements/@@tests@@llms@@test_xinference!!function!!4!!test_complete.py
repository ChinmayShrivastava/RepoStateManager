def test_complete() -> None:
    messages = "test_input"
    dummy = MockXinference("uid", "endpoint")
    response = dummy.complete(messages)
    assert isinstance(response, CompletionResponse)
    assert response.delta is None
    assert response.text == "test_response"

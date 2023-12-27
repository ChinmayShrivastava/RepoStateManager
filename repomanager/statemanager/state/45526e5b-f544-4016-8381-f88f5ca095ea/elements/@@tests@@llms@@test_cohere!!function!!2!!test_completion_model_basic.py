def test_completion_model_basic(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(
        "llama_index.llms.cohere.completion_with_retry", mock_completion_with_retry
    )
    mock_api_key = "fake_key"
    llm = Cohere(model="command", api_key=mock_api_key)
    test_prompt = "test prompt"
    response = llm.complete(test_prompt)
    assert response.text == "\n\nThis is indeed a test"

    monkeypatch.setattr(
        "llama_index.llms.cohere.completion_with_retry", mock_chat_with_retry
    )

    message = ChatMessage(role="user", content=test_prompt)
    chat_response = llm.chat([message])
    assert chat_response.message.content == "\n\nThis is indeed a test"

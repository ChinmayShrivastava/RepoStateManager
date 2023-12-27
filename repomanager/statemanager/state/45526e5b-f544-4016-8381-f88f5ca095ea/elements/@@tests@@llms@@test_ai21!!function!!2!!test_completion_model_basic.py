def test_completion_model_basic(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("ai21.Completion.execute", mock_completion)

    mock_api_key = "fake_key"
    llm = AI21(model="j2-mid", api_key=mock_api_key)

    test_prompt = "This is just a test"
    response = llm.complete(test_prompt)
    assert (
        response.text == "\nThis is a test to see if my text is showing up correctly."
    )

    monkeypatch.setattr("ai21.Completion.execute", mock_chat)

    message = ChatMessage(role="user", content=test_prompt)
    chat_response = llm.chat([message])
    print(chat_response.message.content)
    assert chat_response.message.content == "\nassistant:\nHow can I assist you today?"

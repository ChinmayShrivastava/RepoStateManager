def test_streaming() -> None:
    llm = Anthropic(model="claude-instant-1")
    test_prompt = "test prompt"
    response_gen = llm.stream_complete(test_prompt)
    for r in response_gen:
        assert r.delta is not None
        assert r.text is not None

    message = ChatMessage(role="user", content=test_prompt)
    chat_response_gen = llm.stream_chat([message])
    for r_ in chat_response_gen:
        assert r_.message.content is not None
        assert r_.delta is not None

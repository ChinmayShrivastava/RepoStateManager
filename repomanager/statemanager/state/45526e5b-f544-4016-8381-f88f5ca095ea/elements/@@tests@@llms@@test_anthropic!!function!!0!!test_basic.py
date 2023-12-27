def test_basic() -> None:
    llm = Anthropic(model="claude-instant-1")
    test_prompt = "test prompt"
    response = llm.complete(test_prompt)
    assert len(response.text) > 0

    message = ChatMessage(role="user", content=test_prompt)
    chat_response = llm.chat([message])
    assert chat_response.message.content is not None
    assert len(chat_response.message.content) > 0

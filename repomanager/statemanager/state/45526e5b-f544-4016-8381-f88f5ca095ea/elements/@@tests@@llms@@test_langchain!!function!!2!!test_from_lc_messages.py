def test_from_lc_messages() -> None:
    messages = [
        ChatMessage(content="test system message", role=MessageRole.SYSTEM),
        ChatMessage(content="test human message", role=MessageRole.USER),
        ChatMessage(content="test ai message", role=MessageRole.ASSISTANT),
        ChatMessage(
            content="test function message",
            role=MessageRole.FUNCTION,
            additional_kwargs={"name": "test function"},
        ),
    ]

    lc_messages = to_lc_messages(messages)

    for i in range(len(messages)):
        assert messages[i].content == lc_messages[i].content

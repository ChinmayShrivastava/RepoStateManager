def test_max_tokens() -> None:
    memory = ChatMemoryBuffer.from_defaults(
        chat_history=[USER_CHAT_MESSAGE], token_limit=5
    )

    memory.put(USER_CHAT_MESSAGE)
    assert len(memory.get()) == 2

    # do we limit properly
    memory.put(USER_CHAT_MESSAGE)
    memory.put(USER_CHAT_MESSAGE)
    assert len(memory.get()) == 2

    # does get_all work
    assert len(memory.get_all()) == 4

    # does get return in the correct order?
    memory.put(ChatMessage(role=MessageRole.USER, content="test message2"))
    assert memory.get()[-1].content == "test message2"
    assert len(memory.get()) == 2

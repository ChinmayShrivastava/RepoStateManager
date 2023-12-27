def test_set() -> None:
    memory = ChatMemoryBuffer.from_defaults(chat_history=[USER_CHAT_MESSAGE])

    memory.put(USER_CHAT_MESSAGE)

    assert len(memory.get()) == 2

    memory.set([USER_CHAT_MESSAGE])
    assert len(memory.get()) == 1

def test_put_get() -> None:
    # Given one message in the memory without limit
    memory = ChatMemoryBuffer.from_defaults(chat_history=[USER_CHAT_MESSAGE])

    # When I get the chat history from the memory
    history = memory.get()

    # Then the history should contain the message
    assert len(history) == 1
    assert history[0].content == USER_CHAT_MESSAGE.content

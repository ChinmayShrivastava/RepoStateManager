def test_get_when_initial_tokens_less_than_limit_returns_history() -> None:
    # Given some initial tokens much smaller than token_limit and message tokens
    initial_tokens = 5

    # Given a user message
    memory = ChatMemoryBuffer.from_defaults(
        token_limit=1000, chat_history=[USER_CHAT_MESSAGE]
    )

    # When I get the chat history from the memory
    history = memory.get(initial_tokens)

    # Then the history should contain the message
    assert len(history) == 1
    assert history[0] == USER_CHAT_MESSAGE

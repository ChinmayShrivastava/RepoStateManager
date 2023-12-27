def test_get_when_initial_tokens_same_as_limit_removes_message() -> None:
    # Given some initial tokens equal to the token_limit
    initial_tokens = 5

    # Given a user message
    memory = ChatMemoryBuffer.from_defaults(
        token_limit=initial_tokens, chat_history=[USER_CHAT_MESSAGE]
    )

    # When I get the chat history from the memory
    history = memory.get(initial_tokens)

    # Then the history should be empty
    assert len(history) == 0

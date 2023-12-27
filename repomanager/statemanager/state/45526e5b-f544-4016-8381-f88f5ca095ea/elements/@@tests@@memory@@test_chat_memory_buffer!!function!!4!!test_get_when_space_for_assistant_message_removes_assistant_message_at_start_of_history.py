def test_get_when_space_for_assistant_message_removes_assistant_message_at_start_of_history() -> (
    None
):
    # Given some initial tokens equal to the token_limit minus the user message
    token_limit = 5
    initial_tokens = token_limit - USER_CHAT_MESSAGE_TOKENS

    # Given a user message and an assistant answer
    memory = ChatMemoryBuffer.from_defaults(
        token_limit=token_limit,
        chat_history=[USER_CHAT_MESSAGE, ASSISTANT_CHAT_MESSAGE],
    )

    # When I get the chat history from the memory
    history = memory.get(initial_tokens)

    # Then the history should be empty
    assert len(history) == 0

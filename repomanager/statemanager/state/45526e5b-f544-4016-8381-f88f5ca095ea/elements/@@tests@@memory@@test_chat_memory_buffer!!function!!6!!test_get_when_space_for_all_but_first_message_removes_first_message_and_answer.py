def test_get_when_space_for_all_but_first_message_removes_first_message_and_answer() -> (
    None
):
    # Given some initial tokens equal to the token_limit minus one message and one answer
    token_limit = 10
    history_tokens = (
        ASSISTANT_CHAT_MESSAGE_TOKENS
        + USER_CHAT_MESSAGE_TOKENS
        + SECOND_ASSISTANT_CHAT_MESSAGE_TOKENS
    )
    initial_tokens = token_limit - history_tokens

    # Given two user messages and two assistant answers
    memory = ChatMemoryBuffer.from_defaults(
        token_limit=token_limit,
        chat_history=[
            USER_CHAT_MESSAGE,
            ASSISTANT_CHAT_MESSAGE,
            SECOND_USER_CHAT_MESSAGE,
            SECOND_ASSISTANT_CHAT_MESSAGE,
        ],
    )

    # When I get the chat history from the memory
    history = memory.get(initial_tokens)

    # Then the history should contain the second message and the second answer
    assert len(history) == 2
    assert history[0] == SECOND_USER_CHAT_MESSAGE
    assert history[1] == SECOND_ASSISTANT_CHAT_MESSAGE

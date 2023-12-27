def test_error_user_twice(chat_messages_user_twice: Sequence[ChatMessage]) -> None:
    # should have error if second message is user
    # (or have user twice in a row)
    with pytest.raises(AssertionError):
        messages_to_prompt(chat_messages_user_twice)

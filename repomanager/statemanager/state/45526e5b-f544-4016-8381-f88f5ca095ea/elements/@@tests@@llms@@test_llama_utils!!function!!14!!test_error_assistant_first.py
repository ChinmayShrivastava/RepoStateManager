def test_error_assistant_first(
    chat_messages_assistant_first: Sequence[ChatMessage],
) -> None:
    # should have error if assistant message occurs first
    with pytest.raises(AssertionError):
        messages_to_prompt(chat_messages_assistant_first)

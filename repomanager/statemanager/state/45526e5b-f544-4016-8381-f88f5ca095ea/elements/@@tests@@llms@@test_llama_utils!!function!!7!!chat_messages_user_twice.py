def chat_messages_user_twice() -> Sequence[ChatMessage]:
    # user message twice in a row (after system)
    # should raise error as we expect an assistant message
    # to follow a user message
    return [
        ChatMessage(role=MessageRole.SYSTEM, content="some system message"),
        ChatMessage(role=MessageRole.USER, content="test question 1"),
        ChatMessage(role=MessageRole.USER, content="test question 2"),
    ]

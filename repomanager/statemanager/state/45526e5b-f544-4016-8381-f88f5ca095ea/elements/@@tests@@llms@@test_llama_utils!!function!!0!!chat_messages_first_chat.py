def chat_messages_first_chat() -> Sequence[ChatMessage]:
    # example first chat with system message
    return [
        ChatMessage(role=MessageRole.SYSTEM, content="some system message"),
        ChatMessage(role=MessageRole.USER, content="test question"),
    ]

def chat_messages_third_chat() -> Sequence[ChatMessage]:
    # example third chat with system message
    return [
        ChatMessage(role=MessageRole.SYSTEM, content="some system message"),
        ChatMessage(role=MessageRole.USER, content="test question 1"),
        ChatMessage(role=MessageRole.ASSISTANT, content="some assistant reply 1"),
        ChatMessage(role=MessageRole.USER, content="test question 2"),
        ChatMessage(role=MessageRole.ASSISTANT, content="some assistant reply 2"),
        ChatMessage(role=MessageRole.USER, content="test question 3"),
    ]

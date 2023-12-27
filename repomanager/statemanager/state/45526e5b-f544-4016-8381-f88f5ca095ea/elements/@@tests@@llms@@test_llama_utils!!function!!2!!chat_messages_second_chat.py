def chat_messages_second_chat() -> Sequence[ChatMessage]:
    # example second chat with system message
    return [
        ChatMessage(role=MessageRole.SYSTEM, content="some system message"),
        ChatMessage(role=MessageRole.USER, content="test question 1"),
        ChatMessage(role=MessageRole.ASSISTANT, content="some assistant reply"),
        ChatMessage(role=MessageRole.USER, content="test question 2"),
    ]

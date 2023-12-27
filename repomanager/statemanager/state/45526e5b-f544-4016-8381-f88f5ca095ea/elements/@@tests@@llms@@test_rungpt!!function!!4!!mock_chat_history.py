def mock_chat_history(*args: Any, **kwargs: Any) -> List[ChatMessage]:
    return [
        ChatMessage(
            role=MessageRole.USER,
            message="Hello, my name is zihao, major in artificial intelligence.",
        ),
        ChatMessage(
            role=MessageRole.ASSISTANT,
            message="Hello, what can I do for you?",
        ),
        ChatMessage(
            role=MessageRole.USER,
            message="Could you tell me what is my name and major?",
        ),
    ]

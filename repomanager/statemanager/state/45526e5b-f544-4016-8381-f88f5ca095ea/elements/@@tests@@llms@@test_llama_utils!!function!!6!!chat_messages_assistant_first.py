def chat_messages_assistant_first() -> Sequence[ChatMessage]:
    # assistant message first in chat (after system)
    # should raise error as we expect the first message after any system
    # message to be a user message
    return [
        ChatMessage(role=MessageRole.SYSTEM, content="some system message"),
        ChatMessage(role=MessageRole.ASSISTANT, content="some assistant reply"),
        ChatMessage(role=MessageRole.USER, content="test question"),
    ]

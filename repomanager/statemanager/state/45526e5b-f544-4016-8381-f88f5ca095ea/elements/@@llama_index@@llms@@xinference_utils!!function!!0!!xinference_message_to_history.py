def xinference_message_to_history(message: ChatMessage) -> ChatCompletionMessage:
    return ChatCompletionMessage(role=message.role, content=message.content)

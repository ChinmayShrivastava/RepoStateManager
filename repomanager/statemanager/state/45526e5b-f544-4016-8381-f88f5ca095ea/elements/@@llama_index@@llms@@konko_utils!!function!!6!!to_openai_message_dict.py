def to_openai_message_dict(message: ChatMessage) -> dict:
    """Convert generic message to OpenAI message dict."""
    message_dict = {
        "role": message.role,
        "content": message.content,
    }
    message_dict.update(message.additional_kwargs)

    return message_dict

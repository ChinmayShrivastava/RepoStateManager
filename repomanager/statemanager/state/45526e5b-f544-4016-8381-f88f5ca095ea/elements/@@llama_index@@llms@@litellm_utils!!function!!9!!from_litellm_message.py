def from_litellm_message(message: Message) -> ChatMessage:
    """Convert litellm.utils.Message instance to generic message."""
    role = message.get("role")
    # NOTE: Azure OpenAI returns function calling messages without a content key
    content = message.get("content", None)

    return ChatMessage(role=role, content=content)

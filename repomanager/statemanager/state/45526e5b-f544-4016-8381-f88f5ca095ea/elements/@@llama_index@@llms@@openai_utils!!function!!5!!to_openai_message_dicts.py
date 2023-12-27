def to_openai_message_dicts(
    messages: Sequence[ChatMessage], drop_none: bool = False
) -> List[ChatCompletionMessageParam]:
    """Convert generic messages to OpenAI message dicts."""
    return [
        to_openai_message_dict(message, drop_none=drop_none) for message in messages
    ]

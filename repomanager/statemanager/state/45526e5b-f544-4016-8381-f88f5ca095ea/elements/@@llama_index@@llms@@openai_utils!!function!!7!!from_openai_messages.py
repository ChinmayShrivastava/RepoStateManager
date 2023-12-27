def from_openai_messages(
    openai_messages: Sequence[ChatCompletionMessage],
) -> List[ChatMessage]:
    """Convert openai message dicts to generic messages."""
    return [from_openai_message(message) for message in openai_messages]

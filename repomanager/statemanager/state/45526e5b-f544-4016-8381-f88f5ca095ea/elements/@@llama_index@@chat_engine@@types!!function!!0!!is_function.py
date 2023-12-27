def is_function(message: ChatMessage) -> bool:
    """Utility for ChatMessage responses from OpenAI models."""
    return "tool_calls" in message.additional_kwargs

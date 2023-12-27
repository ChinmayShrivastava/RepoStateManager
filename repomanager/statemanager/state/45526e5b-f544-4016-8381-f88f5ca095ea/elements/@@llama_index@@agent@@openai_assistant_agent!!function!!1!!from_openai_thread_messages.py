def from_openai_thread_messages(thread_messages: List[Any]) -> List[ChatMessage]:
    """From OpenAI thread messages."""
    return [
        from_openai_thread_message(thread_message) for thread_message in thread_messages
    ]

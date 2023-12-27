def messages_to_cohere_history(
    messages: Sequence[ChatMessage],
) -> List[Dict[str, Optional[str]]]:
    return [
        {"user_name": message.role, "message": message.content} for message in messages
    ]

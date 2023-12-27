def messages_to_anyscale_prompt(messages: Sequence[ChatMessage]) -> List[Dict]:
    if len(messages) == 0:
        raise ValueError("Got empty list of messages.")

    return [_message_to_anyscale_prompt(message) for message in messages]

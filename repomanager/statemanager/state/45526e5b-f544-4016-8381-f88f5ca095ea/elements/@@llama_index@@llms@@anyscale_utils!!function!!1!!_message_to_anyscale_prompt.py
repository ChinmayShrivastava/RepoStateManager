def _message_to_anyscale_prompt(message: ChatMessage) -> Dict[str, Any]:
    if message.role == MessageRole.USER:
        prompt = {"role": "user", "content": message.content}
    elif message.role == MessageRole.ASSISTANT:
        prompt = {"role": "assistant", "content": message.content}
    elif message.role == MessageRole.SYSTEM:
        prompt = {"role": "system", "content": message.content}
    elif message.role == MessageRole.FUNCTION:
        raise ValueError(f"Message role {MessageRole.FUNCTION} is not supported.")
    else:
        raise ValueError(f"Unknown message role: {message.role}")

    return prompt

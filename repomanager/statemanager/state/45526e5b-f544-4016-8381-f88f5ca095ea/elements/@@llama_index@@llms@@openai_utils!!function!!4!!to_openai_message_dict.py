def to_openai_message_dict(
    message: ChatMessage, drop_none: bool = False
) -> ChatCompletionMessageParam:
    """Convert generic message to OpenAI message dict."""
    message_dict = {
        "role": message.role,
        "content": message.content,
    }

    # NOTE: openai messages have additional arguments:
    # - function messages have `name`
    # - assistant messages have optional `function_call`
    message_dict.update(message.additional_kwargs)

    null_keys = [key for key, value in message_dict.items() if value is None]
    # if drop_none is True, remove keys with None values
    if drop_none:
        for key in null_keys:
            message_dict.pop(key)

    return message_dict  # type: ignore

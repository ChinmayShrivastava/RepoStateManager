def from_openai_message(openai_message: ChatCompletionMessage) -> ChatMessage:
    """Convert openai message dict to generic message."""
    role = openai_message.role
    # NOTE: Azure OpenAI returns function calling messages without a content key
    content = openai_message.content

    function_call = None  # deprecated in OpenAI v 1.1.0

    additional_kwargs: Dict[str, Any] = {}
    if openai_message.tool_calls is not None:
        tool_calls: List[ChatCompletionMessageToolCall] = openai_message.tool_calls
        additional_kwargs.update(tool_calls=tool_calls)

    return ChatMessage(role=role, content=content, additional_kwargs=additional_kwargs)

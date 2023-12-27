def acompletion_to_chat_decorator(
    func: Callable[..., Awaitable[CompletionResponse]]
) -> Callable[..., Awaitable[ChatResponse]]:
    """Convert a completion function to a chat function."""

    async def wrapper(messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        # normalize input
        prompt = messages_to_prompt(messages)
        completion_response = await func(prompt, **kwargs)
        # normalize output
        return completion_response_to_chat_response(completion_response)

    return wrapper

def achat_to_completion_decorator(
    func: Callable[..., Awaitable[ChatResponse]]
) -> Callable[..., Awaitable[CompletionResponse]]:
    """Convert a chat function to a completion function."""

    async def wrapper(prompt: str, **kwargs: Any) -> CompletionResponse:
        # normalize input
        messages = prompt_to_messages(prompt)
        chat_response = await func(messages, **kwargs)
        # normalize output
        return chat_response_to_completion_response(chat_response)

    return wrapper

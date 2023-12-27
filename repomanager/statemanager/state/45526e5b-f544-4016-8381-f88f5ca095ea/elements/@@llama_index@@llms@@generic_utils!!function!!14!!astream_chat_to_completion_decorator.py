def astream_chat_to_completion_decorator(
    func: Callable[..., Awaitable[ChatResponseAsyncGen]]
) -> Callable[..., Awaitable[CompletionResponseAsyncGen]]:
    """Convert a chat function to a completion function."""

    async def wrapper(prompt: str, **kwargs: Any) -> CompletionResponseAsyncGen:
        # normalize input
        messages = prompt_to_messages(prompt)
        chat_response = await func(messages, **kwargs)
        # normalize output
        return astream_chat_response_to_completion_response(chat_response)

    return wrapper

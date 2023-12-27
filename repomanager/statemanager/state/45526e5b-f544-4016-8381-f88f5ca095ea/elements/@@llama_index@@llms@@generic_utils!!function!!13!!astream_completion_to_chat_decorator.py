def astream_completion_to_chat_decorator(
    func: Callable[..., Awaitable[CompletionResponseAsyncGen]]
) -> Callable[..., Awaitable[ChatResponseAsyncGen]]:
    """Convert a completion function to a chat function."""

    async def wrapper(
        messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        # normalize input
        prompt = messages_to_prompt(messages)
        completion_response = await func(prompt, **kwargs)
        # normalize output
        return astream_completion_response_to_chat_response(completion_response)

    return wrapper

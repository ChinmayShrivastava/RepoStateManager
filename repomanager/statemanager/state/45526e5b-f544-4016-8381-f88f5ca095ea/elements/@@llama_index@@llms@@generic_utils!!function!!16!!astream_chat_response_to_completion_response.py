def astream_chat_response_to_completion_response(
    chat_response_gen: ChatResponseAsyncGen,
) -> CompletionResponseAsyncGen:
    """Convert a stream chat response to a completion response."""

    async def gen() -> CompletionResponseAsyncGen:
        async for response in chat_response_gen:
            yield CompletionResponse(
                text=response.message.content or "",
                additional_kwargs=response.message.additional_kwargs,
                delta=response.delta,
                raw=response.raw,
            )

    return gen()

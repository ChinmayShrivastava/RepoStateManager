def astream_completion_response_to_chat_response(
    completion_response_gen: CompletionResponseAsyncGen,
) -> ChatResponseAsyncGen:
    """Convert a stream completion response to a stream chat response."""

    async def gen() -> ChatResponseAsyncGen:
        async for response in completion_response_gen:
            yield ChatResponse(
                message=ChatMessage(
                    role=MessageRole.ASSISTANT,
                    content=response.text,
                    additional_kwargs=response.additional_kwargs,
                ),
                delta=response.delta,
                raw=response.raw,
            )

    return gen()

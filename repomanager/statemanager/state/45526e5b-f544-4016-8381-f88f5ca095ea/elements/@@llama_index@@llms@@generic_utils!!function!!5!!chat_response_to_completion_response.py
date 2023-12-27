def chat_response_to_completion_response(
    chat_response: ChatResponse,
) -> CompletionResponse:
    """Convert a chat response to a completion response."""
    return CompletionResponse(
        text=chat_response.message.content or "",
        additional_kwargs=chat_response.message.additional_kwargs,
        raw=chat_response.raw,
    )

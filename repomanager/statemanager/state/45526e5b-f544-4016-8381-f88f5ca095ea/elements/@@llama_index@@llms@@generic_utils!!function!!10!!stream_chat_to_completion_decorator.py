def stream_chat_to_completion_decorator(
    func: Callable[..., ChatResponseGen]
) -> Callable[..., CompletionResponseGen]:
    """Convert a chat function to a completion function."""

    def wrapper(prompt: str, **kwargs: Any) -> CompletionResponseGen:
        # normalize input
        messages = prompt_to_messages(prompt)
        chat_response = func(messages, **kwargs)
        # normalize output
        return stream_chat_response_to_completion_response(chat_response)

    return wrapper

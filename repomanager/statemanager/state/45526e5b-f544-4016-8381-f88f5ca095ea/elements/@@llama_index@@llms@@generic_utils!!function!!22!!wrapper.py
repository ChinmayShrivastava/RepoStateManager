    def wrapper(prompt: str, **kwargs: Any) -> CompletionResponse:
        # normalize input
        messages = prompt_to_messages(prompt)
        chat_response = func(messages, **kwargs)
        # normalize output
        return chat_response_to_completion_response(chat_response)
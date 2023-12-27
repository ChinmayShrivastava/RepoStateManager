    def wrapper(messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponseGen:
        # normalize input
        prompt = messages_to_prompt(messages)
        completion_response = func(prompt, **kwargs)
        # normalize output
        return stream_completion_response_to_chat_response(completion_response)

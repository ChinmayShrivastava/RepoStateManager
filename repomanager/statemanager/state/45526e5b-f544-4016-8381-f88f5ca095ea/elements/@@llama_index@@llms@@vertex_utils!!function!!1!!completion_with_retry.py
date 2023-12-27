def completion_with_retry(
    client: Any,
    prompt: Optional[Any],
    max_retries: int = 5,
    chat: bool = False,
    stream: bool = False,
    is_gemini: bool = False,
    params: Any = {},
    **kwargs: Any,
) -> Any:
    """Use tenacity to retry the completion call."""
    retry_decorator = _create_retry_decorator(max_retries=max_retries)

    @retry_decorator
    def _completion_with_retry(**kwargs: Any) -> Any:
        if is_gemini:
            history = params["message_history"] if "message_history" in params else []

            generation = client.start_chat(history=history)
            generation_config = dict(kwargs)
            return generation.send_message(
                prompt, stream=stream, generation_config=generation_config
            )
        elif chat:
            generation = client.start_chat(**params)
            if stream:
                return generation.send_message_streaming(prompt, **kwargs)
            else:
                return generation.send_message(prompt, **kwargs)
        else:
            if stream:
                return client.predict_streaming(prompt, **kwargs)
            else:
                return client.predict(prompt, **kwargs)

    return _completion_with_retry(**kwargs)

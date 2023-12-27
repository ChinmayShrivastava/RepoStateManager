def completion_with_retry(
    client: Any, max_retries: int, chat: bool = False, **kwargs: Any
) -> Any:
    """Use tenacity to retry the completion call."""
    retry_decorator = _create_retry_decorator(max_retries=max_retries)

    @retry_decorator
    def _completion_with_retry(**kwargs: Any) -> Any:
        if chat:
            return client.chat(**kwargs)
        else:
            return client.generate(**kwargs)

    return _completion_with_retry(**kwargs)

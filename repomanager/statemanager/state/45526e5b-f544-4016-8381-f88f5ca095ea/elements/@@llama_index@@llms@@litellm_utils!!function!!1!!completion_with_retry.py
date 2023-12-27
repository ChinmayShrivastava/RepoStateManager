def completion_with_retry(is_chat_model: bool, max_retries: int, **kwargs: Any) -> Any:
    from litellm import completion

    """Use tenacity to retry the completion call."""
    retry_decorator = _create_retry_decorator(max_retries=max_retries)

    @retry_decorator
    def _completion_with_retry(**kwargs: Any) -> Any:
        return completion(**kwargs)

    return _completion_with_retry(**kwargs)

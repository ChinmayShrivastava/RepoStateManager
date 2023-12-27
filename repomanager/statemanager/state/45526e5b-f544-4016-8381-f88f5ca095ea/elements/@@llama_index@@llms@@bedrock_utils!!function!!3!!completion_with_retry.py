def completion_with_retry(
    client: Any,
    model: str,
    request_body: str,
    max_retries: int,
    stream: bool = False,
    **kwargs: Any,
) -> Any:
    """Use tenacity to retry the completion call."""
    retry_decorator = _create_retry_decorator(client=client, max_retries=max_retries)

    @retry_decorator
    def _completion_with_retry(**kwargs: Any) -> Any:
        if stream:
            return client.invoke_model_with_response_stream(
                modelId=model, body=request_body
            )
        return client.invoke_model(modelId=model, body=request_body)

    return _completion_with_retry(**kwargs)

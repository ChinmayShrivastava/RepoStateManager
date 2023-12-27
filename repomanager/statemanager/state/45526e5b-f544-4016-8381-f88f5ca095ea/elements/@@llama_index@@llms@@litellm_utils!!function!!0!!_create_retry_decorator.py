def _create_retry_decorator(max_retries: int) -> Callable[[Any], Any]:
    import litellm

    min_seconds = 4
    max_seconds = 10
    # Wait 2^x * 1 second between each retry starting with
    # 4 seconds, then up to 10 seconds, then 10 seconds afterwards
    return retry(
        reraise=True,
        stop=stop_after_attempt(max_retries),
        wait=wait_exponential(multiplier=1, min=min_seconds, max=max_seconds),
        retry=(
            retry_if_exception_type(litellm.exceptions.Timeout)
            | retry_if_exception_type(litellm.exceptions.APIError)
            | retry_if_exception_type(litellm.exceptions.APIConnectionError)
            | retry_if_exception_type(litellm.exceptions.RateLimitError)
            | retry_if_exception_type(litellm.exceptions.ServiceUnavailableError)
        ),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )

def _create_retry_decorator(max_retries: int) -> Callable[[Any], Any]:
    import google.api_core

    min_seconds = 4
    max_seconds = 10

    return retry(
        reraise=True,
        stop=stop_after_attempt(max_retries),
        wait=wait_exponential(multiplier=1, min=min_seconds, max=max_seconds),
        retry=(
            retry_if_exception_type(google.api_core.exceptions.ServiceUnavailable)
            | retry_if_exception_type(google.api_core.exceptions.ResourceExhausted)
            | retry_if_exception_type(google.api_core.exceptions.Aborted)
            | retry_if_exception_type(google.api_core.exceptions.DeadlineExceeded)
        ),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )

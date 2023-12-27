def _create_retry_decorator(max_retries: int) -> Callable[[Any], Any]:
    min_seconds = 4
    max_seconds = 10
    # Wait 2^x * 1 second between each retry starting with
    # 4 seconds, then up to 10 seconds, then 10 seconds afterwards
    try:
        import cohere
    except ImportError as e:
        raise ImportError(
            "You must install the `cohere` package to use Cohere."
            "Please `pip install cohere`"
        ) from e

    return retry(
        reraise=True,
        stop=stop_after_attempt(max_retries),
        wait=wait_exponential(multiplier=1, min=min_seconds, max=max_seconds),
        retry=(retry_if_exception_type(cohere.error.CohereConnectionError)),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )

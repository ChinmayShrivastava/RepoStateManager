def test_retry_on_conditional_exceptions() -> None:
    """Make sure retry function works on conditional exceptions."""
    global call_count
    call_count = 0
    with pytest.raises(ConditionalException):
        retry_on_exceptions_with_backoff(
            lambda: fn_with_exception(ConditionalException(True)),
            [ErrorToRetry(ConditionalException, lambda e: e.should_retry)],
            max_tries=3,
            min_backoff_secs=0.0,
        )
    assert call_count == 3

    call_count = 0
    with pytest.raises(ConditionalException):
        retry_on_exceptions_with_backoff(
            lambda: fn_with_exception(ConditionalException(False)),
            [ErrorToRetry(ConditionalException, lambda e: e.should_retry)],
            max_tries=3,
            min_backoff_secs=0.0,
        )
    assert call_count == 1

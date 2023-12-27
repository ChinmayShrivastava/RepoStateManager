def time_limit(seconds: int) -> Any:
    """Time limit context manager.

    NOTE: copied from https://github.com/HazyResearch/evaporate.

    """

    def signal_handler(signum: Any, frame: Any) -> Any:
        raise TimeoutException("Timed out!")

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

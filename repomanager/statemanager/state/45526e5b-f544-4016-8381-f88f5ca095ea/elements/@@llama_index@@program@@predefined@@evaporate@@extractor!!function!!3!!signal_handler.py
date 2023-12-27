    def signal_handler(signum: Any, frame: Any) -> Any:
        raise TimeoutException("Timed out!")

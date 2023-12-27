class ConditionalException(Exception):
    """Exception that contains retry attribute."""

    def __init__(self, should_retry: bool) -> None:
        """Initialize with parameters."""
        self.should_retry = should_retry

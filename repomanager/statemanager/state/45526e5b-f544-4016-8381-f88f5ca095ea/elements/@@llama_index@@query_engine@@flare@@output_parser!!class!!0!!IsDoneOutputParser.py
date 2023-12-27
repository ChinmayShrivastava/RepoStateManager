class IsDoneOutputParser(BaseOutputParser):
    """Is done output parser."""

    def __init__(
        self,
        is_done_fn: Optional[Callable[[str], bool]] = None,
        fmt_answer_fn: Optional[Callable[[str], str]] = None,
    ) -> None:
        """Init params."""
        self._is_done_fn = is_done_fn or default_parse_is_done_fn
        self._fmt_answer_fn = fmt_answer_fn or default_format_done_answer

    def parse(self, output: str) -> Any:
        """Parse output."""
        is_done = default_parse_is_done_fn(output)
        if is_done:
            return True, self._fmt_answer_fn(output)
        else:
            return False, output

    def format(self, output: str) -> str:
        """Format a query with structured output formatting instructions."""
        raise NotImplementedError

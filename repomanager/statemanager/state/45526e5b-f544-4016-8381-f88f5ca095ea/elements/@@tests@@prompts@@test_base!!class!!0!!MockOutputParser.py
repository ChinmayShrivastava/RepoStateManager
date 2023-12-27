class MockOutputParser(BaseOutputParser):
    """Mock output parser."""

    def __init__(self, format_string: str) -> None:
        self._format_string = format_string

    def parse(self, output: str) -> Any:
        return {"output": output}

    def format(self, query: str) -> str:
        return query + "\n" + self._format_string

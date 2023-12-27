class MockStreamResponse:
    def __iter__(self) -> Generator[str, Any, None]:
        deltas = ["\n\nThis ", "is indeed", " a test"]
        yield from deltas

class MockEventStream:
    def __iter__(self) -> Generator[dict, None, None]:
        deltas = [b"\\n\\nThis ", b"is indeed", b" a test"]
        for delta in deltas:
            yield {
                "chunk": {
                    "bytes": b'{"outputText":"' + delta + b'",'
                    b'"index":0,"totalOutputTextTokenCount":20,'
                    b'"completionReason":"LENGTH","inputTextTokenCount":7}'
                }
            }

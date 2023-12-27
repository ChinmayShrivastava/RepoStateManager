def mock_completion_stream(*args: Any, **kwargs: Any) -> Generator[str, None, None]:
    # Example taken from rungpt example inferece code on github repo.
    events = [
        str(
            {
                "id": None,
                "object": "text_completion",
                "created": 1692891964,
                "choices": [{"text": "This", "finish_reason": None, "index": 0.0}],
                "prompt": "This",
                "usage": {
                    "completion_tokens": 1,
                    "total_tokens": 7,
                    "prompt_tokens": 6,
                },
            }
        ),
        str(
            {
                "id": None,
                "object": "text_completion",
                "created": 1692891964,
                "choices": [{"text": " is", "finish_reason": None, "index": 0.0}],
                "prompt": " is",
                "usage": {
                    "completion_tokens": 2,
                    "total_tokens": 9,
                    "prompt_tokens": 7,
                },
            }
        ),
        str(
            {
                "id": None,
                "object": "text_completion",
                "created": 1692891964,
                "choices": [{"text": " test.", "finish_reason": None, "index": 0.0}],
                "prompt": " test.",
                "usage": {
                    "completion_tokens": 3,
                    "total_tokens": 11,
                    "prompt_tokens": 8,
                },
            }
        ),
    ]
    yield from events

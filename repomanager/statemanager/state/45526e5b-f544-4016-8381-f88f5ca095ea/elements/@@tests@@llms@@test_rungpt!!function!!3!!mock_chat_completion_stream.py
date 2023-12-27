def mock_chat_completion_stream(
    *args: Any, **kwargs: Any
) -> Generator[str, None, None]:
    # Example taken from rungpt example inferece code on github repo.
    events = [
        str(
            {
                "id": None,
                "object": "chat.completion",
                "created": 1692892378,
                "choices": [
                    {
                        "finish_reason": None,
                        "index": 0.0,
                        "message": {"content": "This", "role": "assistant"},
                    }
                ],
                "prompt": "Mock prompt",
                "usage": {
                    "completion_tokens": 1,
                    "total_tokens": 45,
                    "prompt_tokens": 44,
                },
            }
        ),
        str(
            {
                "id": None,
                "object": "chat.completion",
                "created": 1692892378,
                "choices": [
                    {
                        "finish_reason": None,
                        "index": 0.0,
                        "message": {"content": " is", "role": "assistant"},
                    }
                ],
                "prompt": None,
                "usage": {
                    "completion_tokens": 2,
                    "total_tokens": 47,
                    "prompt_tokens": 45,
                },
            }
        ),
        str(
            {
                "id": None,
                "object": "chat.completion",
                "created": 1692892379,
                "choices": [
                    {
                        "finish_reason": None,
                        "index": 0.0,
                        "message": {"content": " test.", "role": "assistant"},
                    }
                ],
                "prompt": None,
                "usage": {
                    "completion_tokens": 3,
                    "total_tokens": 49,
                    "prompt_tokens": 46,
                },
            }
        ),
    ]
    yield from events

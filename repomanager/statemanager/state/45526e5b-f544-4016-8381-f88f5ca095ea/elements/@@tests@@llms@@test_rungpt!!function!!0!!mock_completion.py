def mock_completion(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    # Example taken from rungpt example inferece code on github repo.
    return {
        "id": None,
        "object": "text_completion",
        "created": 1692891018,
        "choices": [
            {"text": "This is an indeed test.", "finish_reason": "length", "index": 0.0}
        ],
        "prompt": "Once upon a time,",
        "usage": {"completion_tokens": 21, "total_tokens": 27, "prompt_tokens": 6},
    }

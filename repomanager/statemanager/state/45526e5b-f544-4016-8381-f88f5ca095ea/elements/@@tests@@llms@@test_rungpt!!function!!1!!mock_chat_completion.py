def mock_chat_completion(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    # Example taken from rungpt example inferece code on github repo.
    return {
        "id": None,
        "object": "chat.completion",
        "created": 1692892252,
        "choices": [
            {
                "finish_reason": "length",
                "index": 0.0,
                "message": {"content": "This is an indeed test.", "role": "assistant"},
            }
        ],
        "prompt": "Test prompt",
        "usage": {"completion_tokens": 59, "total_tokens": 103, "prompt_tokens": 44},
    }

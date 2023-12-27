def mock_chat_with_retry(*args: Any, **kwargs: Any) -> dict:
    return cohere.responses.Chat.from_dict(
        {
            "chatlog": None,
            "citations": None,
            "conversation_id": None,
            "documents": None,
            "generation_id": "357d15b3-9bd4-4170-9439-2e4cef2242c8",
            "id": "25c3632f-2d2a-4e15-acbd-804b976d0568",
            "is_search_required": None,
            "message": "test prompt",
            "meta": {"api_version": {"version": "1"}},
            "preamble": None,
            "prompt": None,
            "response_id": "25c3632f-2d2a-4e15-acbd-804b976d0568",
            "search_queries": None,
            "search_results": None,
            "text": "\n\nThis is indeed a test",
            "token_count": {
                "billed_tokens": 66,
                "prompt_tokens": 64,
                "response_tokens": 9,
                "total_tokens": 73,
            },
        },
        client=None,
        message="test_prompt",
    )

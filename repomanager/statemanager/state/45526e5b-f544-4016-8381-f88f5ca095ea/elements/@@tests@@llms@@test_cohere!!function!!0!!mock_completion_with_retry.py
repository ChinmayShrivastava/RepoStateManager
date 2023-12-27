def mock_completion_with_retry(*args: Any, **kwargs: Any) -> dict:
    # Example taken from https://docs.cohere.com/reference/generate
    return cohere.responses.Generations.from_dict(
        {
            "id": "21caa4c4-6b88-45f7-b144-14ef4985384c",
            "generations": [
                {
                    "id": "b5e2bb70-bc9c-4f86-a22e-5b5fd13a3482",
                    "text": "\n\nThis is indeed a test",
                    "finish_reason": "COMPLETE",
                }
            ],
            "prompt": "test prompt",
            "meta": {"api_version": {"version": "1"}},
        },
        return_likelihoods=False,
    )

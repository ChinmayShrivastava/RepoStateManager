def mock_completion(text: str) -> Completion:
    return Completion(
        id="cmpl-abc123",
        object="text_completion",
        created=1677858242,
        model=STUB_MODEL_NAME,
        usage={"prompt_tokens": 13, "completion_tokens": 7, "total_tokens": 20},
        choices=[
            CompletionChoice(
                text=text,
                finish_reason="stop",
                index=0,
            )
        ],
    )

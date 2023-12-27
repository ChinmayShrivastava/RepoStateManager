def mock_completion(text: str) -> Completion:
    return Completion(
        id="chatcmpl-abc123",
        object="text_completion",
        created=1677858242,
        model="gpt-3.5-turbo-0301",
        usage={"prompt_tokens": 13, "completion_tokens": 7, "total_tokens": 20},
        choices=[
            CompletionChoice(
                text=text,
                finish_reason="stop",
                index=0,
            )
        ],
    )

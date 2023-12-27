def mock_completion_v1(*args: Any, **kwargs: Any) -> Completion:
    return Completion(
        id="cmpl-uqkvlQyYK7bGYrRHQ0eXlWi7",
        object="text_completion",
        created=1589478378,
        model="text-davinci-003",
        choices=[
            CompletionChoice(
                text="\n\nThis is indeed a test",
                index=0,
                logprobs=None,
                finish_reason="length",
            )
        ],
        usage=CompletionUsage(prompt_tokens=5, completion_tokens=7, total_tokens=12),
    )

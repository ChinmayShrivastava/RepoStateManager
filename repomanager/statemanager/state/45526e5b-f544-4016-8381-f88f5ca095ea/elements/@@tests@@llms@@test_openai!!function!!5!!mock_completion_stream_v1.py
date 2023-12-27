def mock_completion_stream_v1(
    *args: Any, **kwargs: Any
) -> Generator[Completion, None, None]:
    responses = [
        Completion(
            id="cmpl-uqkvlQyYK7bGYrRHQ0eXlWi7",
            object="text_completion",
            created=1589478378,
            model="text-davinci-003",
            choices=[CompletionChoice(text="1", finish_reason="stop", index=0)],
        ),
        Completion(
            id="cmpl-uqkvlQyYK7bGYrRHQ0eXlWi7",
            object="text_completion",
            created=1589478378,
            model="text-davinci-003",
            choices=[CompletionChoice(text="2", finish_reason="stop", index=0)],
        ),
    ]
    yield from responses

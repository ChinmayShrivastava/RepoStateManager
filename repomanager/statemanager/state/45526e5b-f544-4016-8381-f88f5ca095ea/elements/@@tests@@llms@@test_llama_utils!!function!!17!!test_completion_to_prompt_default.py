def test_completion_to_prompt_default() -> None:
    # test prompt creation from completion without system prompt and use default
    completion = "test completion"
    prompt = completion_to_prompt(completion)
    assert prompt == (
        f"{BOS} {B_INST} {B_SYS} {DEFAULT_SYSTEM_PROMPT.strip()} {E_SYS} "
        f"{completion} {E_INST}"
    )

def test_completion_to_prompt() -> None:
    # test prompt creation from completion with system prompt
    completion = "test completion"
    system_prompt = "test system prompt"
    prompt = completion_to_prompt(completion, system_prompt=system_prompt)
    assert prompt == (
        f"{BOS} {B_INST} {B_SYS} {system_prompt} {E_SYS} {completion} {E_INST}"
    )

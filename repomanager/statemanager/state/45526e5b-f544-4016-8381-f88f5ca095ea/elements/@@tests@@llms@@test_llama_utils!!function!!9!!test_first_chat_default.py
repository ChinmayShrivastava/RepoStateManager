def test_first_chat_default(
    chat_messages_first_chat_no_system: Sequence[ChatMessage],
) -> None:
    # test first chat prompt creation without system prompt and use default
    prompt = messages_to_prompt(chat_messages_first_chat_no_system)
    assert prompt == (
        f"{BOS} {B_INST} {B_SYS} {DEFAULT_SYSTEM_PROMPT.strip()} {E_SYS} "
        f"test question {E_INST}"
    )

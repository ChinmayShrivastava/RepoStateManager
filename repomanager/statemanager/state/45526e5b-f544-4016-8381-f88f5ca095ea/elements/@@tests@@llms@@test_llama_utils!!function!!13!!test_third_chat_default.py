def test_third_chat_default(
    chat_messages_third_chat_no_system: Sequence[ChatMessage],
) -> None:
    # test third chat prompt creation without system prompt and use default
    prompt = messages_to_prompt(chat_messages_third_chat_no_system)
    assert prompt == (
        f"{BOS} {B_INST} {B_SYS} {DEFAULT_SYSTEM_PROMPT.strip()} {E_SYS} "
        f"test question 1 {E_INST} some assistant reply 1 {EOS}"
        f"{BOS} {B_INST} test question 2 {E_INST} some assistant reply 2 {EOS}"
        f"{BOS} {B_INST} test question 3 {E_INST}"
    )

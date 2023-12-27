def test_first_chat(chat_messages_first_chat: Sequence[ChatMessage]) -> None:
    # test first chat prompt creation with system prompt
    prompt = messages_to_prompt(chat_messages_first_chat)
    assert prompt == (
        f"{BOS} {B_INST} {B_SYS} some system message {E_SYS} test question {E_INST}"
    )

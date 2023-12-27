def test_second_chat(chat_messages_second_chat: Sequence[ChatMessage]) -> None:
    # test second chat prompt creation with system prompt
    prompt = messages_to_prompt(chat_messages_second_chat)
    assert prompt == (
        f"{BOS} {B_INST} {B_SYS} some system message {E_SYS} "
        f"test question 1 {E_INST} some assistant reply {EOS}"
        f"{BOS} {B_INST} test question 2 {E_INST}"
    )

def test_third_chat(chat_messages_third_chat: Sequence[ChatMessage]) -> None:
    # test third chat prompt creation with system prompt
    prompt = messages_to_prompt(chat_messages_third_chat)
    assert prompt == (
        f"{BOS} {B_INST} {B_SYS} some system message {E_SYS} "
        f"test question 1 {E_INST} some assistant reply 1 {EOS}"
        f"{BOS} {B_INST} test question 2 {E_INST} some assistant reply 2 {EOS}"
        f"{BOS} {B_INST} test question 3 {E_INST}"
    )

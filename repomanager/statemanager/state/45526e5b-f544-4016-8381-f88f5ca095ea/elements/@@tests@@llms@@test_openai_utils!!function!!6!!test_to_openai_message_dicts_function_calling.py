def test_to_openai_message_dicts_function_calling(
    chat_messages_with_function_calling: List[ChatMessage],
    openi_message_dicts_with_function_calling: List[ChatCompletionMessageParam],
) -> None:
    message_dicts = to_openai_message_dicts(chat_messages_with_function_calling)
    assert message_dicts == openi_message_dicts_with_function_calling

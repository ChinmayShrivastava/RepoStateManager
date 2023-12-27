def test_from_openai_messages_function_calling_azure(
    azure_openai_message_dicts_with_function_calling: List[ChatCompletionMessage],
    azure_chat_messages_with_function_calling: List[ChatMessage],
) -> None:
    chat_messages = from_openai_messages(
        azure_openai_message_dicts_with_function_calling
    )
    assert chat_messages == azure_chat_messages_with_function_calling

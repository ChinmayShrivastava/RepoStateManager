def chat_messages_first_chat_no_system(
    chat_messages_first_chat: Sequence[ChatMessage],
) -> Sequence[ChatMessage]:
    # example first chat without system message
    return chat_messages_first_chat[1:]

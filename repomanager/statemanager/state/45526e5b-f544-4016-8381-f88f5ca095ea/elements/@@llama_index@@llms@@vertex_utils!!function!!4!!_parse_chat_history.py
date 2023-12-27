def _parse_chat_history(history: Any, is_gemini: bool) -> Any:
    """Parse a sequence of messages into history.

    Args:
        history: The list of messages to re-create the history of the chat.

    Returns:
        A parsed chat history.

    Raises:
        ValueError: If a sequence of message has a SystemMessage not at the
        first place.
    """
    from vertexai.language_models import ChatMessage

    vertex_messages, context = [], None
    for i, message in enumerate(history):
        if i == 0 and message.role == MessageRole.SYSTEM:
            if is_gemini:
                raise ValueError("Gemini model don't support system messages")
            context = message.content
        elif message.role == MessageRole.ASSISTANT or message.role == MessageRole.USER:
            if is_gemini:
                from llama_index.llms.vertex_gemini_utils import (
                    convert_chat_message_to_gemini_content,
                )

                vertex_messages.append(convert_chat_message_to_gemini_content(message))
            else:
                vertex_message = ChatMessage(
                    content=message.content,
                    author="bot" if message.role == MessageRole.ASSISTANT else "user",
                )
                vertex_messages.append(vertex_message)
        else:
            raise ValueError(
                f"Unexpected message with type {type(message)} at the position {i}."
            )
    if len(vertex_messages) % 2 != 0:
        raise ValueError("total no of messages should be even")

    return {"context": context, "message_history": vertex_messages}

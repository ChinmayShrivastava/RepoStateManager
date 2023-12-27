def _parse_message(message: ChatMessage, is_gemini: bool) -> Any:
    if is_gemini:
        from llama_index.llms.vertex_gemini_utils import (
            convert_chat_message_to_gemini_content,
        )

        return convert_chat_message_to_gemini_content(message)
    else:
        return message.content

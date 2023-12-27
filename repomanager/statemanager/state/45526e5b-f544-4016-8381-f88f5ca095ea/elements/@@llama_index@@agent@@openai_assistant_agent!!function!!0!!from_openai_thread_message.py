def from_openai_thread_message(thread_message: Any) -> ChatMessage:
    """From OpenAI thread message."""
    from openai.types.beta.threads import MessageContentText, ThreadMessage

    thread_message = cast(ThreadMessage, thread_message)

    # we don't have a way of showing images, just do text for now
    text_contents = [
        t for t in thread_message.content if isinstance(t, MessageContentText)
    ]
    text_content_str = " ".join([t.text.value for t in text_contents])

    return ChatMessage(
        role=thread_message.role,
        content=text_content_str,
        additional_kwargs={
            "thread_message": thread_message,
            "thread_id": thread_message.thread_id,
            "assistant_id": thread_message.assistant_id,
            "id": thread_message.id,
            "metadata": thread_message.metadata,
        },
    )

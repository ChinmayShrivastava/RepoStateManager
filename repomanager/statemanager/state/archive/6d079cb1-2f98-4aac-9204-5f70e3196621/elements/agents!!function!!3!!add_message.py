def add_message(threadid, message_raw):
    message = client.beta.threads.messages.create(
        thread_id=threadid,
        role=message_raw["role"],
        content=message_raw["content"],
    )
    return message

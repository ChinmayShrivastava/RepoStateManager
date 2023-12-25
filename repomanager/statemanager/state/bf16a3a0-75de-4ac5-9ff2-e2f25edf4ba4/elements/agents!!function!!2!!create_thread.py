def create_thread(messages_raw):
    messages = []
    for message_raw in messages_raw:
        message = {
            "role": message_raw["role"],
            "content": message_raw["content"]
        }
        messages.append(message)
    thread = client.beta.threads.create(
        messages=messages
    )
    return thread

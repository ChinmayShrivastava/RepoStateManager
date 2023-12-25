def get_response(threadid):
    messages = client.beta.threads.messages.list(
        thread_id=threadid
    )
    return messages
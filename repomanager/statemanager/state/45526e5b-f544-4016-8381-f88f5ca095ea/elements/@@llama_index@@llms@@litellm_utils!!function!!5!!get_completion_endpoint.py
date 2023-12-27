def get_completion_endpoint(is_chat_model: bool) -> CompletionClientType:
    from litellm import completion

    return completion

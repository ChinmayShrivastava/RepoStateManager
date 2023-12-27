def get_completion_endpoint(is_chat_model: bool) -> Any:
    import konko

    if is_chat_model:
        return konko.ChatCompletion
    else:
        return konko.Completion

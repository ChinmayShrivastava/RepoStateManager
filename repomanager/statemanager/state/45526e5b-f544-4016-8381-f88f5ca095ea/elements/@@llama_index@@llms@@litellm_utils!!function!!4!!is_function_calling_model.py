def is_function_calling_model(model: str) -> bool:
    is_chat_model_ = is_chat_model(model)
    is_old = "0314" in model or "0301" in model
    return is_chat_model_ and not is_old

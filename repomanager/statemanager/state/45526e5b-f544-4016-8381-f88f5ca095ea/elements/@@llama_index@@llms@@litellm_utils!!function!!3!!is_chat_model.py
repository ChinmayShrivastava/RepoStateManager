def is_chat_model(model: str) -> bool:
    import litellm

    return model in litellm.model_list

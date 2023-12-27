def is_chat_model(model: str) -> bool:
    """Check if a given model is a chat-based language model.

    This function takes a model name or identifier as input and determines whether
    the model is designed for chat-based language generation, conversation, or
    interaction.

    Args:
        model (str): The name or identifier of the model to be checked.

    Returns:
        bool: True if the provided model is a chat-based language model,
        False otherwise.
    """
    return model in CHAT_MODELS

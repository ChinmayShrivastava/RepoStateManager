def is_chat_model(llm: BaseLLM) -> bool:
    return llm.metadata.is_chat_model

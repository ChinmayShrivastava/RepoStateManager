def is_chat_model(llm: BaseLanguageModel) -> bool:
    return isinstance(llm, BaseChatModel)

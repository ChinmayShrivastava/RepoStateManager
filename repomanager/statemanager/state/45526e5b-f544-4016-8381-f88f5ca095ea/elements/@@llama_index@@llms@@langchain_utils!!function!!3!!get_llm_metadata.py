def get_llm_metadata(llm: BaseLanguageModel) -> LLMMetadata:
    """Get LLM metadata from llm."""
    if not isinstance(llm, BaseLanguageModel):
        raise ValueError("llm must be an instance of langchain.llms.base.LLM")

    is_chat_model_ = is_chat_model(llm)

    if isinstance(llm, OpenAI):
        return LLMMetadata(
            context_window=openai_modelname_to_contextsize(llm.model_name),
            num_output=llm.max_tokens,
            is_chat_model=is_chat_model_,
            model_name=llm.model_name,
        )
    elif isinstance(llm, ChatAnyscale):
        return LLMMetadata(
            context_window=anyscale_modelname_to_contextsize(llm.model_name),
            num_output=llm.max_tokens or -1,
            is_chat_model=is_chat_model_,
            model_name=llm.model_name,
        )
    elif isinstance(llm, ChatOpenAI):
        return LLMMetadata(
            context_window=openai_modelname_to_contextsize(llm.model_name),
            num_output=llm.max_tokens or -1,
            is_chat_model=is_chat_model_,
            model_name=llm.model_name,
        )
    elif isinstance(llm, Cohere):
        # June 2023: Cohere's supported max input size for Generation models is 2048
        # Reference: <https://docs.cohere.com/docs/tokens>
        return LLMMetadata(
            context_window=COHERE_CONTEXT_WINDOW,
            num_output=llm.max_tokens,
            is_chat_model=is_chat_model_,
            model_name=llm.model,
        )
    elif isinstance(llm, AI21):
        # June 2023:
        #   AI21's supported max input size for
        #   J2 models is 8K (8192 tokens to be exact)
        # Reference: <https://docs.ai21.com/changelog/increased-context-length-for-j2-foundation-models>
        return LLMMetadata(
            context_window=AI21_J2_CONTEXT_WINDOW,
            num_output=llm.maxTokens,
            is_chat_model=is_chat_model_,
            model_name=llm.model,
        )
    else:
        return LLMMetadata(is_chat_model=is_chat_model_)

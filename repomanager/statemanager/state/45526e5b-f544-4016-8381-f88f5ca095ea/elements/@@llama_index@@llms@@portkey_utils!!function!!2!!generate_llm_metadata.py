def generate_llm_metadata(llm: "LLMOptions") -> LLMMetadata:
    """
    Generate metadata for a Language Model (LLM) instance.

    This function takes an instance of a Language Model (LLM) and generates
    metadata based on the provided instance. The metadata includes information
    such as the context window, number of output tokens, chat model status,
    and model name.

    Parameters:
        llm (LLM): An instance of a Language Model (LLM) from which metadata
            will be generated.

    Returns:
        LLMMetadata: A data structure containing metadata attributes such as
            context window, number of output tokens, chat model status, and
            model name.

    Raises:
        ValueError: If the provided 'llm' is not an instance of
        llama_index.llms.base.LLM.
    """
    try:
        from portkey import LLMOptions
    except ImportError as exc:
        raise ImportError(IMPORT_ERROR_MESSAGE) from exc
    if not isinstance(llm, LLMOptions):
        raise ValueError("llm must be an instance of portkey.LLMOptions")

    return LLMMetadata(
        _context_window=modelname_to_contextsize(llm.model or ""),
        is_chat_model=is_chat_model(llm.model or ""),
        model_name=llm.model,
    )

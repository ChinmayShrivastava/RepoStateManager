def get_llm(response: "PortkeyResponse", llms: List["LLMOptions"]) -> "LLMOptions":
    # TODO: Update this logic over here.
    try:
        from portkey import LLMOptions
    except ImportError as exc:
        raise ImportError(IMPORT_ERROR_MESSAGE) from exc
    fallback_llm = LLMOptions.construct()
    for llm in llms:
        model = llm.model

        if model == response.model:
            fallback_llm = llm
            break

    if fallback_llm is None:
        raise ValueError("Failed to get the fallback LLM")
    return fallback_llm

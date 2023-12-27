def get_model(model: str) -> LLM:
    llm: LLM
    if model in OPENAI_MODELS:
        llm = OpenAI(model=model)
    elif model in ANTHROPIC_MODELS:
        llm = Anthropic(model=model)
    elif model in LLAMA_MODELS:
        model_dict = {
            "llama13b-v2-chat": LLAMA_13B_V2_CHAT,
            "llama70b-v2-chat": LLAMA_70B_V2_CHAT,
        }
        replicate_model = model_dict[model]
        llm = Replicate(
            model=replicate_model,
            temperature=0.01,
            context_window=4096,
            # override message representation for llama 2
            messages_to_prompt=messages_to_prompt,
        )
    else:
        raise ValueError(f"Unknown model {model}")
    return llm

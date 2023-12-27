def get_query_instruct_for_model_name(model_name: Optional[str]) -> str:
    """Get query text instruction for a given model name."""
    if model_name in INSTRUCTOR_MODELS:
        return DEFAULT_QUERY_INSTRUCTION
    if model_name in BGE_MODELS:
        if "zh" in model_name:
            return DEFAULT_QUERY_BGE_INSTRUCTION_ZH
        return DEFAULT_QUERY_BGE_INSTRUCTION_EN
    return ""

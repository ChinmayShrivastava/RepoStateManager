def build_lm_format_enforcer_function(
    llm: LLM, character_level_parser: "CharacterLevelParser"
) -> Callable:
    """Prepare for using the LM format enforcer.
    This builds the processing function that will be injected into the LLM to
    activate the LM Format Enforcer.
    """
    if isinstance(llm, HuggingFaceLLM):
        from lmformatenforcer.integrations.transformers import (
            build_transformers_prefix_allowed_tokens_fn,
        )

        return build_transformers_prefix_allowed_tokens_fn(
            llm._tokenizer, character_level_parser
        )
    if isinstance(llm, LlamaCPP):
        from llama_cpp import LogitsProcessorList
        from lmformatenforcer.integrations.llamacpp import (
            build_llamacpp_logits_processor,
        )

        return LogitsProcessorList(
            [build_llamacpp_logits_processor(llm._model, character_level_parser)]
        )
    raise ValueError("Unsupported LLM type")

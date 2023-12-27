def activate_lm_format_enforcer(
    llm: LLM, lm_format_enforcer_fn: Callable
) -> Iterator[None]:
    """Activate the LM Format Enforcer for the given LLM.

    with activate_lm_format_enforcer(llm, lm_format_enforcer_fn):
        llm.complete(...)
    """
    if isinstance(llm, HuggingFaceLLM):
        generate_kwargs_key = "prefix_allowed_tokens_fn"
    elif isinstance(llm, LlamaCPP):
        generate_kwargs_key = "logits_processor"
    else:
        raise ValueError("Unsupported LLM type")
    llm.generate_kwargs[generate_kwargs_key] = lm_format_enforcer_fn

    try:
        # This is where the user code will run
        yield
    finally:
        # We remove the token enforcer function from the generate_kwargs at the end
        # in case other code paths use the same llm object.
        del llm.generate_kwargs[generate_kwargs_key]

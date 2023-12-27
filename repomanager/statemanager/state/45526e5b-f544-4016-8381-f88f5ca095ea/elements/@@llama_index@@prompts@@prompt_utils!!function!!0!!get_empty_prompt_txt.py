def get_empty_prompt_txt(prompt: BasePromptTemplate) -> str:
    """Get empty prompt text.

    Substitute empty strings in parts of the prompt that have
    not yet been filled out. Skip variables that have already
    been partially formatted. This is used to compute the initial tokens.

    """
    partial_kargs = prompt.kwargs
    empty_kwargs = {v: "" for v in prompt.template_vars if v not in partial_kargs}
    all_kwargs = {**partial_kargs, **empty_kwargs}
    return prompt.format(llm=None, **all_kwargs)

def get_biggest_prompt(prompts: List[BasePromptTemplate]) -> BasePromptTemplate:
    """Get biggest prompt.

    Oftentimes we need to fetch the biggest prompt, in order to
    be the most conservative about chunking text. This
    is a helper utility for that.

    """
    empty_prompt_txts = [get_empty_prompt_txt(prompt) for prompt in prompts]
    empty_prompt_txt_lens = [len(txt) for txt in empty_prompt_txts]
    return prompts[empty_prompt_txt_lens.index(max(empty_prompt_txt_lens))]

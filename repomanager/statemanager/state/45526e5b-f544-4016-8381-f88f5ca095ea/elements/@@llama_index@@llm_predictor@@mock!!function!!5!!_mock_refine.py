def _mock_refine(max_tokens: int, prompt: BasePromptTemplate, prompt_args: Dict) -> str:
    """Mock refine."""
    # tokens in response shouldn't be larger than tokens in
    # `existing_answer` + `context_msg`
    # NOTE: if existing_answer is not in prompt_args, we need to get it from the prompt
    if "existing_answer" not in prompt_args:
        existing_answer = prompt.kwargs["existing_answer"]
    else:
        existing_answer = prompt_args["existing_answer"]
    num_ctx_tokens = len(get_tokenizer()(prompt_args["context_msg"]))
    num_exist_tokens = len(get_tokenizer()(existing_answer))
    token_limit = min(num_ctx_tokens + num_exist_tokens, max_tokens)
    return " ".join(["answer"] * token_limit)

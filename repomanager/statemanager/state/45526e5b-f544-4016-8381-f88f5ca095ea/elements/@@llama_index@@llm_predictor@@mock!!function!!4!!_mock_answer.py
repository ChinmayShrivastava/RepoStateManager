def _mock_answer(max_tokens: int, prompt_args: Dict) -> str:
    """Mock answer."""
    # tokens in response shouldn't be larger than tokens in `text`
    num_ctx_tokens = len(get_tokenizer()(prompt_args["context_str"]))
    token_limit = min(num_ctx_tokens, max_tokens)
    return " ".join(["answer"] * token_limit)

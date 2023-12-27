def _mock_summary_predict(max_tokens: int, prompt_args: Dict) -> str:
    """Mock summary predict."""
    # tokens in response shouldn't be larger than tokens in `context_str`
    num_text_tokens = len(get_tokenizer()(prompt_args["context_str"]))
    token_limit = min(num_text_tokens, max_tokens)
    return " ".join(["summary"] * token_limit)

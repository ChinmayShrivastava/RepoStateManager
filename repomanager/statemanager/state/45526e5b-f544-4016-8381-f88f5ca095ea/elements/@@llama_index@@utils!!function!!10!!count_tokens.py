def count_tokens(text: str) -> int:
    tokenizer = get_tokenizer()
    tokens = tokenizer(text)
    return len(tokens)

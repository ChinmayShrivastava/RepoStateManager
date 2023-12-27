def set_global_tokenizer(tokenizer: Union[Tokenizer, Callable[[str], list]]) -> None:
    import llama_index

    if isinstance(tokenizer, Tokenizer):
        llama_index.global_tokenizer = tokenizer.encode
    else:
        llama_index.global_tokenizer = tokenizer

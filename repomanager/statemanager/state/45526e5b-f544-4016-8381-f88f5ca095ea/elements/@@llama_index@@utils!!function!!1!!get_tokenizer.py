def get_tokenizer() -> Callable[[str], List]:
    import llama_index

    if llama_index.global_tokenizer is None:
        tiktoken_import_err = (
            "`tiktoken` package not found, please run `pip install tiktoken`"
        )
        try:
            import tiktoken
        except ImportError:
            raise ImportError(tiktoken_import_err)

        # set tokenizer cache temporarily
        should_revert = False
        if "TIKTOKEN_CACHE_DIR" not in os.environ:
            should_revert = True
            os.environ["TIKTOKEN_CACHE_DIR"] = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "_static/tiktoken_cache",
            )

        enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
        tokenizer = partial(enc.encode, allowed_special="all")
        set_global_tokenizer(tokenizer)

        if should_revert:
            del os.environ["TIKTOKEN_CACHE_DIR"]

    assert llama_index.global_tokenizer is not None
    return llama_index.global_tokenizer

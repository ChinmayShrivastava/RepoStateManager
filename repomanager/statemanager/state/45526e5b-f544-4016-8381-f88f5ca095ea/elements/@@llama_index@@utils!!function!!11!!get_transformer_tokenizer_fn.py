def get_transformer_tokenizer_fn(model_name: str) -> Callable[[str], List[str]]:
    """
    Args:
        model_name(str): the model name of the tokenizer.
                        For instance, fxmarty/tiny-llama-fast-tokenizer.
    """
    try:
        from transformers import AutoTokenizer
    except ImportError:
        raise ValueError(
            "`transformers` package not found, please run `pip install transformers`"
        )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return tokenizer.tokenize

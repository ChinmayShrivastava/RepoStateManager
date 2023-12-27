def get_default_tokenizer() -> Callable:
    """Get default tokenizer.

    NOTE: taken from https://www.pinecone.io/learn/hybrid-search-intro/.

    """
    from transformers import BertTokenizerFast

    orig_tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
    # set some default arguments, so input is just a list of strings
    return partial(
        orig_tokenizer,
        padding=True,
        truncation=True,
        max_length=512,
    )

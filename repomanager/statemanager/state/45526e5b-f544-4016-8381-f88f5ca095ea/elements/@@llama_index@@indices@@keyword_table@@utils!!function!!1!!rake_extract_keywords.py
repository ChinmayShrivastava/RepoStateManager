def rake_extract_keywords(
    text_chunk: str,
    max_keywords: Optional[int] = None,
    expand_with_subtokens: bool = True,
) -> Set[str]:
    """Extract keywords with RAKE."""
    try:
        import nltk
    except ImportError:
        raise ImportError("Please install nltk: `pip install nltk`")
    try:
        from rake_nltk import Rake
    except ImportError:
        raise ImportError("Please install rake_nltk: `pip install rake_nltk`")

    r = Rake(
        sentence_tokenizer=nltk.tokenize.sent_tokenize,
        word_tokenizer=nltk.tokenize.wordpunct_tokenize,
    )
    r.extract_keywords_from_text(text_chunk)
    keywords = r.get_ranked_phrases()[:max_keywords]
    if expand_with_subtokens:
        return set(expand_tokens_with_subtokens(keywords))
    else:
        return set(keywords)

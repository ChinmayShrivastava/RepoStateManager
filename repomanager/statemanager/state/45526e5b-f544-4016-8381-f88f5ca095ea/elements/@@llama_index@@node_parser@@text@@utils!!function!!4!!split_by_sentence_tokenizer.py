def split_by_sentence_tokenizer() -> Callable[[str], List[str]]:
    import nltk

    tokenizer = nltk.tokenize.PunktSentenceTokenizer()

    # get the spans and then return the sentences
    # using the start index of each span
    # instead of using end, use the start of the next span if available
    def split(text: str) -> List[str]:
        spans = list(tokenizer.span_tokenize(text))
        sentences = []
        for i, span in enumerate(spans):
            start = span[0]
            if i < len(spans) - 1:
                end = spans[i + 1][0]
            else:
                end = len(text)
            sentences.append(text[start:end])

        return sentences

    return split

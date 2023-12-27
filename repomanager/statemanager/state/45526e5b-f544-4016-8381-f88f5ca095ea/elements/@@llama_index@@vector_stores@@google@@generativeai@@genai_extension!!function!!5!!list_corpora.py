def list_corpora(
    *,
    client: genai.RetrieverServiceClient,
) -> Iterator[Corpus]:
    for corpus in client.list_corpora(
        genai.ListCorporaRequest(page_size=_config.page_size)
    ):
        yield Corpus.from_corpus(corpus)

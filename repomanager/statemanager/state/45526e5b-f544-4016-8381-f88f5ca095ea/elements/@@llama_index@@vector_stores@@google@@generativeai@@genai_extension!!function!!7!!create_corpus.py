def create_corpus(
    *,
    corpus_id: Optional[str] = None,
    display_name: Optional[str] = None,
    client: genai.RetrieverServiceClient,
) -> Corpus:
    name: Optional[str]
    if corpus_id is not None:
        name = str(EntityName(corpus_id=corpus_id))
    else:
        name = None

    new_display_name = display_name or f"Untitled {datetime.datetime.now()}"

    new_corpus = client.create_corpus(
        genai.CreateCorpusRequest(
            corpus=genai.Corpus(name=name, display_name=new_display_name)
        )
    )

    return Corpus.from_corpus(new_corpus)

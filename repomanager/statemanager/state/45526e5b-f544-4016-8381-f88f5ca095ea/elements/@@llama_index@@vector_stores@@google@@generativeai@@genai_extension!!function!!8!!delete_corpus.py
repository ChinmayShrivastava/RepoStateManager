def delete_corpus(
    *,
    corpus_id: str,
    client: genai.RetrieverServiceClient,
) -> None:
    client.delete_corpus(
        genai.DeleteCorpusRequest(name=str(EntityName(corpus_id=corpus_id)), force=True)
    )

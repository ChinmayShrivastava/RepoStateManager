def get_corpus(
    *,
    corpus_id: str,
    client: genai.RetrieverServiceClient,
) -> Optional[Corpus]:
    try:
        corpus = client.get_corpus(
            genai.GetCorpusRequest(name=str(EntityName(corpus_id=corpus_id)))
        )
        return Corpus.from_corpus(corpus)
    except Exception as e:
        # If the corpus does not exist, the server returns a permission error.
        if not isinstance(e, gapi_exception.PermissionDenied):
            raise
        _logger.warning(f"Corpus {corpus_id} not found: {e}")
        return None

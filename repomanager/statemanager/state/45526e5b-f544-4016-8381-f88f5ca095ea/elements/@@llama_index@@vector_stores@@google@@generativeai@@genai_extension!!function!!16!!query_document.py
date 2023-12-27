def query_document(
    *,
    corpus_id: str,
    document_id: str,
    query: str,
    k: int = 4,
    filter: Optional[Dict[str, Any]] = None,
    client: genai.RetrieverServiceClient,
) -> List[genai.RelevantChunk]:
    response = client.query_document(
        genai.QueryDocumentRequest(
            name=str(EntityName(corpus_id=corpus_id, document_id=document_id)),
            query=query,
            metadata_filters=_convert_filter(filter),
            results_count=k,
        )
    )
    return list(response.relevant_chunks)

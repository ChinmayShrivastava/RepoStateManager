def get_document(
    *,
    corpus_id: str,
    document_id: str,
    client: genai.RetrieverServiceClient,
) -> Optional[Document]:
    try:
        document = client.get_document(
            genai.GetDocumentRequest(
                name=str(EntityName(corpus_id=corpus_id, document_id=document_id))
            )
        )
        return Document.from_document(document)
    except Exception as e:
        if not isinstance(e, gapi_exception.NotFound):
            raise
        _logger.warning(f"Document {document_id} in corpus {corpus_id} not found: {e}")
        return None

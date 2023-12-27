def delete_document(
    *,
    corpus_id: str,
    document_id: str,
    client: genai.RetrieverServiceClient,
) -> None:
    client.delete_document(
        genai.DeleteDocumentRequest(
            name=str(EntityName(corpus_id=corpus_id, document_id=document_id)),
            force=True,
        )
    )

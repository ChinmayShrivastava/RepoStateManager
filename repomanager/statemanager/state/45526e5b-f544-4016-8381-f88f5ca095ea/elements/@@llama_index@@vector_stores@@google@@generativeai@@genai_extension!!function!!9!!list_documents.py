def list_documents(
    *,
    corpus_id: str,
    client: genai.RetrieverServiceClient,
) -> Iterator[Document]:
    for document in client.list_documents(
        genai.ListDocumentsRequest(
            parent=str(EntityName(corpus_id=corpus_id)), page_size=_DEFAULT_PAGE_SIZE
        )
    ):
        yield Document.from_document(document)

def create_document(
    *,
    corpus_id: str,
    document_id: Optional[str] = None,
    display_name: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    client: genai.RetrieverServiceClient,
) -> Document:
    name: Optional[str]
    if document_id is not None:
        name = str(EntityName(corpus_id=corpus_id, document_id=document_id))
    else:
        name = None

    new_display_name = display_name or f"Untitled {datetime.datetime.now()}"
    new_metadatas = _convert_to_metadata(metadata) if metadata else None

    new_document = client.create_document(
        genai.CreateDocumentRequest(
            parent=str(EntityName(corpus_id=corpus_id)),
            document=genai.Document(
                name=name, display_name=new_display_name, custom_metadata=new_metadatas
            ),
        )
    )

    return Document.from_document(new_document)

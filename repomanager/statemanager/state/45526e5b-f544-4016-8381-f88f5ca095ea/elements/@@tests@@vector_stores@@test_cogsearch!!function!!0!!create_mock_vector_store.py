def create_mock_vector_store(
    search_client: Any,
    index_name: Optional[str] = None,
    index_management: IndexManagement = IndexManagement.NO_VALIDATION,
) -> CognitiveSearchVectorStore:
    return CognitiveSearchVectorStore(
        search_or_index_client=search_client,
        id_field_key="id",
        chunk_field_key="content",
        embedding_field_key="embedding",
        metadata_string_field_key="li_jsonMetadata",
        doc_id_field_key="li_doc_id",
        index_name=index_name,
        index_management=index_management,
    )

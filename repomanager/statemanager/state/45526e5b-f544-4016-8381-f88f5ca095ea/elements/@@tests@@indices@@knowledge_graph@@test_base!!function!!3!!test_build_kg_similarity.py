def test_build_kg_similarity(
    _patch_extract_triplets: Any,
    documents: List[Document],
    mock_service_context: ServiceContext,
) -> None:
    """Test build knowledge graph."""
    mock_service_context.embed_model = MockEmbedding()

    index = KnowledgeGraphIndex.from_documents(
        documents, include_embeddings=True, service_context=mock_service_context
    )
    # get embedding dict from KG index struct
    rel_text_embeddings = index.index_struct.embedding_dict

    # check that all rel_texts were embedded
    assert len(rel_text_embeddings) == 3
    for rel_text, embedding in rel_text_embeddings.items():
        assert embedding == MockEmbedding().get_text_embedding(rel_text)

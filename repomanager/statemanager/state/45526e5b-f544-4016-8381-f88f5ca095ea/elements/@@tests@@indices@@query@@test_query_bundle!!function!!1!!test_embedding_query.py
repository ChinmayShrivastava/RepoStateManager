def test_embedding_query(
    documents: List[Document],
    mock_service_context: ServiceContext,
) -> None:
    """Test embedding query."""
    mock_service_context.embed_model = MockEmbedding()
    index = SummaryIndex.from_documents(documents, service_context=mock_service_context)

    # test embedding query
    query_bundle = QueryBundle(
        query_str="What is?",
        custom_embedding_strs=[
            "It is what it is.",
            "The meaning of life",
        ],
    )
    retriever = index.as_retriever(retriever_mode="embedding", similarity_top_k=1)
    nodes = retriever.retrieve(query_bundle)
    assert len(nodes) == 1
    assert nodes[0].node.get_content() == "Correct."

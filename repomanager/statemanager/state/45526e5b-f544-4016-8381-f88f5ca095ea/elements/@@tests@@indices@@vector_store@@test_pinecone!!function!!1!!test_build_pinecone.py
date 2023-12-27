def test_build_pinecone(
    documents: List[Document],
    mock_service_context: ServiceContext,
) -> None:
    """Test build VectorStoreIndex with PineconeVectorStore."""
    storage_context = get_pinecone_storage_context()
    index = VectorStoreIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        service_context=mock_service_context,
        tokenizer=mock_tokenizer,
    )

    retriever = index.as_retriever(similarity_top_k=1)
    nodes = retriever.retrieve("What is?")
    assert len(nodes) == 1
    assert nodes[0].node.get_content() == "This is another test."

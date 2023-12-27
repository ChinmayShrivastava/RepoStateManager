def test_as_retriever(
    documents: List[Document],
    mock_service_context: ServiceContext,
) -> None:
    summary_index = SummaryIndex.from_documents(
        documents, service_context=mock_service_context
    )
    default_retriever = summary_index.as_retriever(
        retriever_mode=ListRetrieverMode.DEFAULT
    )
    assert isinstance(default_retriever, BaseRetriever)

    embedding_retriever = summary_index.as_retriever(
        retriever_mode=ListRetrieverMode.EMBEDDING
    )
    assert isinstance(embedding_retriever, BaseRetriever)

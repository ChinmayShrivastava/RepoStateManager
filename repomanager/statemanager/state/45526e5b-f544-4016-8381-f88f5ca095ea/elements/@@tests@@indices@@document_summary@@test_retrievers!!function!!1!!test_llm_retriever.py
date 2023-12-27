def test_llm_retriever(
    index: DocumentSummaryIndex,
) -> None:
    retriever = index.as_retriever(retriever_mode=DocumentSummaryRetrieverMode.LLM)
    assert isinstance(retriever, DocumentSummaryIndexLLMRetriever)
    results = retriever.retrieve("Test query")
    assert len(results) == 1

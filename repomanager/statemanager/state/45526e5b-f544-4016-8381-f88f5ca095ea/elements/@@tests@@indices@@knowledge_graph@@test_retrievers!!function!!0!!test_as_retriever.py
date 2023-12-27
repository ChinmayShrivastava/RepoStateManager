def test_as_retriever(
    _patch_extract_triplets: Any,
    documents: List[Document],
    mock_service_context: ServiceContext,
) -> None:
    """Test query."""
    graph_store = SimpleGraphStore()
    storage_context = StorageContext.from_defaults(graph_store=graph_store)
    index = KnowledgeGraphIndex.from_documents(
        documents, service_context=mock_service_context, storage_context=storage_context
    )
    retriever: KGTableRetriever = index.as_retriever()  # type: ignore
    nodes = retriever.retrieve(QueryBundle("foo"))
    # when include_text is True, the first node is the raw text
    # the second node is the query
    rel_initial_text = (
        f"The following are knowledge sequence in max depth"
        f" {retriever.graph_store_query_depth} "
        f"in the form of directed graph like:\n"
        f"`subject -[predicate]->, object, <-[predicate_next_hop]-,"
        f" object_next_hop ...`"
    )

    raw_text = "['foo', 'is', 'bar']"
    query = rel_initial_text + "\n" + raw_text
    assert len(nodes) == 2
    assert nodes[1].node.get_content() == query

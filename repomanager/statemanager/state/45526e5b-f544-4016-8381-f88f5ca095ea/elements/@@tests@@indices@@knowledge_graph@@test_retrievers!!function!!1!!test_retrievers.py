def test_retrievers(
    _patch_extract_triplets: Any,
    documents: List[Document],
    mock_service_context: ServiceContext,
) -> None:
    # test specific retriever class
    graph_store = SimpleGraphStore()
    storage_context = StorageContext.from_defaults(graph_store=graph_store)

    index = KnowledgeGraphIndex.from_documents(
        documents, service_context=mock_service_context, storage_context=storage_context
    )
    retriever = KGTableRetriever(
        index,
        query_keyword_extract_template=MOCK_QUERY_KEYWORD_EXTRACT_PROMPT,
        graph_store=graph_store,
    )
    query_bundle = QueryBundle(query_str="foo", custom_embedding_strs=["foo"])
    nodes = retriever.retrieve(query_bundle)
    assert (
        nodes[1].node.get_content()
        == "The following are knowledge sequence in max depth 2"
        " in the form of directed graph like:\n"
        "`subject -[predicate]->, object, <-[predicate_next_hop]-,"
        " object_next_hop ...`"
        "\n['foo', 'is', 'bar']"
    )

def test_retrieve_similarity(
    _patch_extract_triplets: Any,
    documents: List[Document],
    mock_service_context: ServiceContext,
) -> None:
    """Test query."""
    mock_service_context.embed_model = MockEmbedding()
    graph_store = SimpleGraphStore()
    storage_context = StorageContext.from_defaults(graph_store=graph_store)

    index = KnowledgeGraphIndex.from_documents(
        documents,
        include_embeddings=True,
        service_context=mock_service_context,
        storage_context=storage_context,
    )
    retriever = KGTableRetriever(index, similarity_top_k=2, graph_store=graph_store)

    # returns only two rel texts to use for generating response
    # uses hyrbid query by default
    nodes = retriever.retrieve(QueryBundle("foo"))
    assert (
        nodes[1].node.get_content()
        == "The following are knowledge sequence in max depth 2"
        " in the form of directed graph like:\n"
        "`subject -[predicate]->, object, <-[predicate_next_hop]-,"
        " object_next_hop ...`"
        "\n['foo', 'is', 'bar']"
    )

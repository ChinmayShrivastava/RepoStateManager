def test_recursive_query_vector_table_async(
    allow_networking: Any,
    documents: List[Document],
    mock_service_context: ServiceContext,
    index_kwargs: Dict,
) -> None:
    """Test async query of table index over vector indices."""
    vector_kwargs = index_kwargs["vector"]
    table_kwargs = index_kwargs["table"]
    # try building a tree for a group of 4, then a list
    # use a diff set of documents
    # try building a list for every two, then a tree
    vector1 = VectorStoreIndex.from_documents(
        documents[0:2], service_context=mock_service_context, **vector_kwargs
    )
    vector2 = VectorStoreIndex.from_documents(
        documents[2:4], service_context=mock_service_context, **vector_kwargs
    )
    list3 = VectorStoreIndex.from_documents(
        documents[4:6], service_context=mock_service_context, **vector_kwargs
    )
    list4 = VectorStoreIndex.from_documents(
        documents[6:8], service_context=mock_service_context, **vector_kwargs
    )
    indices = [vector1, vector2, list3, list4]

    summaries = [
        "foo bar",
        "apple orange",
        "toronto london",
        "cat dog",
    ]

    graph = ComposableGraph.from_indices(
        SimpleKeywordTableIndex,
        children_indices=indices,
        index_summaries=summaries,
        service_context=mock_service_context,
        **table_kwargs
    )

    custom_query_engines = {
        index.index_id: index.as_query_engine(similarity_top_k=1) for index in indices
    }
    custom_query_engines[graph.root_id] = graph.root_index.as_query_engine(
        similarity_top_k=1
    )

    query_engine = graph.as_query_engine(custom_query_engines=custom_query_engines)
    task = query_engine.aquery("Cat?")
    response = asyncio.run(task)
    assert str(response) == ("Cat?:Cat?:This is a test v2.")

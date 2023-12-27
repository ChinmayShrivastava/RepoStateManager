def test_recursive_query_list_table(
    documents: List[Document],
    mock_service_context: ServiceContext,
    index_kwargs: Dict,
) -> None:
    """Test query."""
    list_kwargs = index_kwargs["list"]
    table_kwargs = index_kwargs["table"]
    # try building a tree for a group of 4, then a list
    # use a diff set of documents
    # try building a list for every two, then a tree
    list1 = SummaryIndex.from_documents(
        documents[0:2], service_context=mock_service_context, **list_kwargs
    )
    list2 = SummaryIndex.from_documents(
        documents[2:4], service_context=mock_service_context, **list_kwargs
    )
    list3 = SummaryIndex.from_documents(
        documents[4:6], service_context=mock_service_context, **list_kwargs
    )
    list4 = SummaryIndex.from_documents(
        documents[6:8], service_context=mock_service_context, **list_kwargs
    )
    summaries = [
        "foo bar",
        "apple orange",
        "toronto london",
        "cat dog",
    ]

    graph = ComposableGraph.from_indices(
        SimpleKeywordTableIndex,
        [list1, list2, list3, list4],
        index_summaries=summaries,
        service_context=mock_service_context,
        **table_kwargs
    )
    assert isinstance(graph, ComposableGraph)
    query_str = "Foo?"
    query_engine = graph.as_query_engine()
    response = query_engine.query(query_str)
    assert str(response) == ("Foo?:Foo?:This is a test v2.:This is another test.")
    query_str = "Orange?"
    response = query_engine.query(query_str)
    assert str(response) == ("Orange?:Orange?:This is a test.:Hello world.")
    query_str = "Cat?"
    response = query_engine.query(query_str)
    assert str(response) == ("Cat?:Cat?:This is another test.:This is a test v2.")

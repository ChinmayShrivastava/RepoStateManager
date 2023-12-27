def test_recursive_query_table_list(
    documents: List[Document],
    mock_service_context: ServiceContext,
    index_kwargs: Dict,
) -> None:
    """Test query."""
    list_kwargs = index_kwargs["list"]
    table_kwargs = index_kwargs["table"]
    # try building a tree for a group of 4, then a list
    # use a diff set of documents
    table1 = SimpleKeywordTableIndex.from_documents(
        documents[4:6], service_context=mock_service_context, **table_kwargs
    )
    table2 = SimpleKeywordTableIndex.from_documents(
        documents[2:3], service_context=mock_service_context, **table_kwargs
    )
    summaries = [
        "table_summary1",
        "table_summary2",
    ]

    graph = ComposableGraph.from_indices(
        SummaryIndex,
        [table1, table2],
        index_summaries=summaries,
        service_context=mock_service_context,
        **list_kwargs
    )
    assert isinstance(graph, ComposableGraph)
    query_str = "World?"
    query_engine = graph.as_query_engine()
    response = query_engine.query(query_str)
    assert str(response) == ("World?:World?:Hello world.:Empty Response")

    query_str = "Test?"
    response = query_engine.query(query_str)
    assert str(response) == ("Test?:Test?:This is a test.:Test?:This is a test.")

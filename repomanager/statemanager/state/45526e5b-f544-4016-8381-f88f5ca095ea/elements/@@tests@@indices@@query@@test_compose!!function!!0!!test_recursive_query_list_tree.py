def test_recursive_query_list_tree(
    documents: List[Document],
    mock_service_context: ServiceContext,
    index_kwargs: Dict,
) -> None:
    """Test query."""
    list_kwargs = index_kwargs["list"]
    tree_kwargs = index_kwargs["tree"]
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

    summary1 = "summary1"
    summary2 = "summary2"
    summary3 = "summary3"
    summary4 = "summary4"
    summaries = [summary1, summary2, summary3, summary4]

    # there are two root nodes in this tree: one containing [list1, list2]
    # and the other containing [list3, list4]
    graph = ComposableGraph.from_indices(
        TreeIndex,
        [
            list1,
            list2,
            list3,
            list4,
        ],
        index_summaries=summaries,
        service_context=mock_service_context,
        **tree_kwargs
    )
    assert isinstance(graph, ComposableGraph)
    query_str = "What is?"
    # query should first pick the left root node, then pick list1
    # within list1, it should go through the first document and second document
    query_engine = graph.as_query_engine()
    response = query_engine.query(query_str)
    assert str(response) == (
        "What is?:What is?:This is a test v2.:This is another test."
    )

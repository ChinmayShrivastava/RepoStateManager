def test_recursive_query_tree_list(
    documents: List[Document],
    mock_service_context: ServiceContext,
    index_kwargs: Dict,
) -> None:
    """Test query."""
    list_kwargs = index_kwargs["list"]
    tree_kwargs = index_kwargs["tree"]
    # try building a tree for a group of 4, then a list
    # use a diff set of documents
    tree1 = TreeIndex.from_documents(
        documents[2:6], service_context=mock_service_context, **tree_kwargs
    )
    tree2 = TreeIndex.from_documents(
        documents[:2] + documents[6:],
        service_context=mock_service_context,
        **tree_kwargs
    )
    summaries = [
        "tree_summary1",
        "tree_summary2",
    ]

    # there are two root nodes in this tree: one containing [list1, list2]
    # and the other containing [list3, list4]
    graph = ComposableGraph.from_indices(
        SummaryIndex,
        [tree1, tree2],
        index_summaries=summaries,
        service_context=mock_service_context,
        **list_kwargs
    )
    assert isinstance(graph, ComposableGraph)
    query_str = "What is?"
    # query should first pick the left root node, then pick list1
    # within list1, it should go through the first document and second document
    query_engine = graph.as_query_engine()
    response = query_engine.query(query_str)
    assert str(response) == (
        "What is?:What is?:This is a test.:What is?:This is a test v2."
    )

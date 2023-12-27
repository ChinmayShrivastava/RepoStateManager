def test_recursive_query_vector_table_query_configs(
    documents: List[Document],
    mock_service_context: ServiceContext,
    index_kwargs: Dict,
) -> None:
    """Test query.

    Difference with above test is we specify query config params and
    assert that they're passed in.

    """
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
    assert isinstance(vector1.index_struct, IndexStruct)
    assert isinstance(vector2.index_struct, IndexStruct)
    vector1.index_struct.index_id = "vector1"
    vector2.index_struct.index_id = "vector2"
    summaries = [
        "foo bar",
        "apple orange",
    ]

    graph = ComposableGraph.from_indices(
        SimpleKeywordTableIndex,
        [vector1, vector2],
        index_summaries=summaries,
        service_context=mock_service_context,
        **table_kwargs
    )
    assert isinstance(graph, ComposableGraph)

    custom_query_engines = {
        "keyword_table": graph.root_index.as_query_engine(
            query_keyword_extract_template=MOCK_QUERY_KEYWORD_EXTRACT_PROMPT
        ),
        "vector1": vector1.as_query_engine(similarity_top_k=2),
        "vector2": vector2.as_query_engine(similarity_top_k=2),
    }

    query_engine = graph.as_query_engine(custom_query_engines=custom_query_engines)
    response = query_engine.query("Foo?")  # type: ignore
    assert str(response) == ("Foo?:Foo?:This is another test.:This is a test v2.")

    response = query_engine.query("Orange?")  # type: ignore
    assert str(response) == ("Orange?:Orange?:This is a test.:Hello world.")

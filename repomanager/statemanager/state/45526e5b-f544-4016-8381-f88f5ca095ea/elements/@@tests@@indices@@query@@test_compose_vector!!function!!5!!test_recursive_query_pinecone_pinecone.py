def test_recursive_query_pinecone_pinecone(
    documents: List[Document],
    mock_service_context: ServiceContext,
    index_kwargs: Dict,
) -> None:
    """Test composing pinecone index on top of pinecone index."""
    pinecone_kwargs = index_kwargs["pinecone"]
    # try building a tree for a group of 4, then a list
    # use a diff set of documents
    # try building a list for every two, then a tree
    pinecone1 = VectorStoreIndex.from_documents(
        documents[0:2],
        storage_context=get_pinecone_storage_context(),
        service_context=mock_service_context,
        **pinecone_kwargs
    )
    pinecone2 = VectorStoreIndex.from_documents(
        documents[2:4],
        storage_context=get_pinecone_storage_context(),
        service_context=mock_service_context,
        **pinecone_kwargs
    )
    pinecone3 = VectorStoreIndex.from_documents(
        documents[4:6],
        storage_context=get_pinecone_storage_context(),
        service_context=mock_service_context,
        **pinecone_kwargs
    )
    pinecone4 = VectorStoreIndex.from_documents(
        documents[6:8],
        storage_context=get_pinecone_storage_context(),
        service_context=mock_service_context,
        **pinecone_kwargs
    )
    indices = [pinecone1, pinecone2, pinecone3, pinecone4]

    summary1 = "foo bar"
    summary2 = "apple orange"
    summary3 = "toronto london"
    summary4 = "cat dog"
    summaries = [summary1, summary2, summary3, summary4]

    graph = ComposableGraph.from_indices(
        VectorStoreIndex,
        children_indices=indices,
        index_summaries=summaries,
        storage_context=get_pinecone_storage_context(),
        service_context=mock_service_context,
        **pinecone_kwargs
    )
    custom_query_engines = {
        index.index_id: index.as_query_engine(similarity_top_k=1) for index in indices
    }
    custom_query_engines[graph.root_id] = graph.root_index.as_query_engine(
        similarity_top_k=1
    )
    query_engine = graph.as_query_engine(custom_query_engines=custom_query_engines)
    query_str = "Foo?"
    response = query_engine.query(query_str)
    # assert str(response) == ("Foo?:Foo?:This is another test.")
    query_str = "Orange?"
    response = query_engine.query(query_str)
    # assert str(response) == ("Orange?:Orange?:This is a test.")
    query_str = "Cat?"
    response = query_engine.query(query_str)
    assert str(response) == ("Cat?:Cat?:This is a test v2.")

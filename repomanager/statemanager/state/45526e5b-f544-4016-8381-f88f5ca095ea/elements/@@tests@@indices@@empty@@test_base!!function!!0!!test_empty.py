def test_empty(
    mock_service_context: ServiceContext,
) -> None:
    """Test build list."""
    empty_index = EmptyIndex(service_context=mock_service_context)
    assert isinstance(empty_index.index_struct, EmptyIndexStruct)

    retriever = empty_index.as_retriever()
    nodes = retriever.retrieve("What is?")
    assert len(nodes) == 0

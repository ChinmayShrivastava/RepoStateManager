def test_build_tree_multiple(
    mock_service_context: ServiceContext,
    struct_kwargs: Dict,
) -> None:
    """Test build tree."""
    new_docs = [
        Document(text="Hello world.\nThis is a test."),
        Document(text="This is another test.\nThis is a test v2."),
    ]
    index_kwargs, _ = struct_kwargs
    tree = TreeIndex.from_documents(
        new_docs, service_context=mock_service_context, **index_kwargs
    )
    assert len(tree.index_struct.all_nodes) == 6
    # check contents of nodes
    nodes = tree.docstore.get_nodes(list(tree.index_struct.all_nodes.values()))
    assert nodes[0].get_content() == "Hello world."
    assert nodes[1].get_content() == "This is a test."
    assert nodes[2].get_content() == "This is another test."
    assert nodes[3].get_content() == "This is a test v2."

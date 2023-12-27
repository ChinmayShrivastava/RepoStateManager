def test_build_tree_with_embed(
    documents: List[Document],
    mock_service_context: ServiceContext,
    struct_kwargs: Dict,
) -> None:
    """Test build tree."""
    index_kwargs, _ = struct_kwargs
    doc_text = (
        "Hello world.\n"
        "This is a test.\n"
        "This is another test.\n"
        "This is a test v2."
    )
    document = Document(text=doc_text, embedding=[0.1, 0.2, 0.3])
    tree = TreeIndex.from_documents(
        [document], service_context=mock_service_context, **index_kwargs
    )
    assert len(tree.index_struct.all_nodes) == 6
    # check contents of nodes
    all_nodes = tree.docstore.get_node_dict(tree.index_struct.all_nodes)
    assert all_nodes[0].get_content() == "Hello world."
    assert all_nodes[1].get_content() == "This is a test."
    assert all_nodes[2].get_content() == "This is another test."
    assert all_nodes[3].get_content() == "This is a test v2."
    # make sure all leaf nodes have embeddings
    for i in range(4):
        assert all_nodes[i].embedding == [0.1, 0.2, 0.3]
    assert all_nodes[4].get_content() == ("Hello world.\nThis is a test.")
    assert all_nodes[5].get_content() == ("This is another test.\nThis is a test v2.")

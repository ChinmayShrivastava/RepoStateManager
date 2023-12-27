def test_build_tree(
    documents: List[Document],
    mock_service_context: ServiceContext,
    struct_kwargs: Dict,
) -> None:
    """Test build tree."""
    index_kwargs, _ = struct_kwargs
    tree = TreeIndex.from_documents(
        documents, service_context=mock_service_context, **index_kwargs
    )
    assert len(tree.index_struct.all_nodes) == 6
    # check contents of nodes

    nodes = tree.docstore.get_nodes(list(tree.index_struct.all_nodes.values()))
    assert nodes[0].get_content() == "Hello world."
    assert nodes[1].get_content() == "This is a test."
    assert nodes[2].get_content() == "This is another test."
    assert nodes[3].get_content() == "This is a test v2."
    assert nodes[4].get_content() == ("Hello world.\nThis is a test.")
    assert nodes[5].get_content() == ("This is another test.\nThis is a test v2.")

    # test ref doc info
    all_ref_doc_info = tree.ref_doc_info
    for idx, ref_doc_id in enumerate(all_ref_doc_info.keys()):
        assert documents[idx].doc_id == ref_doc_id

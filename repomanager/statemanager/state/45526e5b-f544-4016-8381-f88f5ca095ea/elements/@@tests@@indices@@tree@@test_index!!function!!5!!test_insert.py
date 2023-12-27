def test_insert(
    documents: List[Document],
    mock_service_context: ServiceContext,
    struct_kwargs: Dict,
) -> None:
    """Test insert."""
    index_kwargs, _ = struct_kwargs
    tree = TreeIndex.from_documents(
        documents, service_context=mock_service_context, **index_kwargs
    )

    # test insert
    new_doc = Document(text="This is a new doc.", id_="new_doc")
    tree.insert(new_doc)
    # Before:
    # Left root node: "Hello world.\nThis is a test."
    # "Hello world.", "This is a test" are two children of the left root node
    # After:
    # "Hello world.\nThis is a test\n.\nThis is a new doc." is the left root node
    # "Hello world", "This is a test\n.This is a new doc." are the children
    # of the left root node.
    # "This is a test", "This is a new doc." are the children of
    # "This is a test\n.This is a new doc."
    left_root = _get_left_or_right_node(tree.docstore, tree.index_struct, None)
    assert left_root.get_content() == "Hello world.\nThis is a test."
    left_root2 = _get_left_or_right_node(tree.docstore, tree.index_struct, left_root)
    right_root2 = _get_left_or_right_node(
        tree.docstore, tree.index_struct, left_root, left=False
    )
    assert left_root2.get_content() == "Hello world."
    assert right_root2.get_content() == "This is a test.\nThis is a new doc."
    left_root3 = _get_left_or_right_node(tree.docstore, tree.index_struct, right_root2)
    right_root3 = _get_left_or_right_node(
        tree.docstore, tree.index_struct, right_root2, left=False
    )
    assert left_root3.get_content() == "This is a test."
    assert right_root3.get_content() == "This is a new doc."
    assert right_root3.ref_doc_id == "new_doc"

    # test insert from empty (no_id)
    tree = TreeIndex.from_documents(
        [], service_context=mock_service_context, **index_kwargs
    )
    new_doc = Document(text="This is a new doc.")
    tree.insert(new_doc)
    nodes = tree.docstore.get_nodes(list(tree.index_struct.all_nodes.values()))
    assert len(nodes) == 1
    assert nodes[0].get_content() == "This is a new doc."

    # test insert from empty (with_id)
    tree = TreeIndex.from_documents(
        [], service_context=mock_service_context, **index_kwargs
    )
    new_doc = Document(text="This is a new doc.", id_="new_doc_test")
    tree.insert(new_doc)
    assert len(tree.index_struct.all_nodes) == 1
    nodes = tree.docstore.get_nodes(list(tree.index_struct.all_nodes.values()))
    assert nodes[0].get_content() == "This is a new doc."
    assert nodes[0].ref_doc_id == "new_doc_test"

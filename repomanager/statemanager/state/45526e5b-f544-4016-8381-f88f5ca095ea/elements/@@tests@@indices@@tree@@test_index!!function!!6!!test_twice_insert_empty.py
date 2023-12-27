def test_twice_insert_empty(
    mock_service_context: ServiceContext,
) -> None:
    """# test twice insert from empty (with_id)."""
    tree = TreeIndex.from_documents([], service_context=mock_service_context)

    # test first insert
    new_doc = Document(text="This is a new doc.", id_="new_doc")
    tree.insert(new_doc)
    # test second insert
    new_doc_second = Document(text="This is a new doc2.", id_="new_doc_2")
    tree.insert(new_doc_second)
    assert len(tree.index_struct.all_nodes) == 2

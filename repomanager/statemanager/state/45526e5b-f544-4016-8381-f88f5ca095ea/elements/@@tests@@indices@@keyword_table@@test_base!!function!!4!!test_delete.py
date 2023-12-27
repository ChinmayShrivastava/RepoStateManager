def test_delete(
    mock_service_context: ServiceContext,
) -> None:
    """Test insert."""
    new_documents = [
        Document(text="Hello world.\nThis is a test.", id_="test_id_1"),
        Document(text="This is another test.", id_="test_id_2"),
        Document(text="This is a test v2.", id_="test_id_3"),
    ]

    # test delete
    table = SimpleKeywordTableIndex.from_documents(
        new_documents, service_context=mock_service_context
    )
    # test delete
    table.delete_ref_doc("test_id_1")
    assert len(table.index_struct.table.keys()) == 6
    assert len(table.index_struct.table["this"]) == 2

    # test node contents after delete
    nodes = table.docstore.get_nodes(list(table.index_struct.node_ids))
    node_texts = {n.get_content() for n in nodes}
    assert node_texts == {"This is another test.", "This is a test v2."}

    table = SimpleKeywordTableIndex.from_documents(
        new_documents, service_context=mock_service_context
    )

    # test ref doc info
    all_ref_doc_info = table.ref_doc_info
    for doc_id in all_ref_doc_info:
        assert doc_id in ("test_id_1", "test_id_2", "test_id_3")

    # test delete
    table.delete_ref_doc("test_id_2")
    assert len(table.index_struct.table.keys()) == 7
    assert len(table.index_struct.table["this"]) == 2

    # test node contents after delete
    nodes = table.docstore.get_nodes(list(table.index_struct.node_ids))
    node_texts = {n.get_content() for n in nodes}
    assert node_texts == {"Hello world.", "This is a test.", "This is a test v2."}

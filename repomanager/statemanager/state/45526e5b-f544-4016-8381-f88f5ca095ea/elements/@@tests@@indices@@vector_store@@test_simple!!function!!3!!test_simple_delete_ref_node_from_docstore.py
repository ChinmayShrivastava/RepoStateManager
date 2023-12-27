def test_simple_delete_ref_node_from_docstore(
    mock_service_context: ServiceContext,
) -> None:
    """Test delete VectorStoreIndex."""
    new_documents = [
        Document(text="This is a test.", id_="test_id_1"),
        Document(text="This is another test.", id_="test_id_2"),
    ]
    index = VectorStoreIndex.from_documents(
        documents=new_documents, service_context=mock_service_context
    )
    assert isinstance(index, VectorStoreIndex)

    docstore = index.docstore.get_ref_doc_info("test_id_1")

    assert docstore is not None

    # test delete
    index.delete_ref_doc("test_id_1", delete_from_docstore=True)

    docstore = index.docstore.get_ref_doc_info("test_id_1")

    assert docstore is None

def test_list_delete(
    documents: List[Document],
    mock_service_context: ServiceContext,
) -> None:
    """Test insert to list and then delete."""
    new_documents = [
        Document(text="Hello world.\nThis is a test.", id_="test_id_1"),
        Document(text="This is another test.", id_="test_id_2"),
        Document(text="This is a test v2.", id_="test_id_3"),
    ]

    summary_index = SummaryIndex.from_documents(
        new_documents, service_context=mock_service_context
    )

    # test ref doc info for three docs
    all_ref_doc_info = summary_index.ref_doc_info
    for idx, ref_doc_id in enumerate(all_ref_doc_info.keys()):
        assert new_documents[idx].doc_id == ref_doc_id

    # delete from documents
    summary_index.delete_ref_doc("test_id_1")
    assert len(summary_index.index_struct.nodes) == 2
    nodes = summary_index.docstore.get_nodes(summary_index.index_struct.nodes)
    assert nodes[0].ref_doc_id == "test_id_2"
    assert nodes[0].get_content() == "This is another test."
    assert nodes[1].ref_doc_id == "test_id_3"
    assert nodes[1].get_content() == "This is a test v2."
    # check that not in docstore anymore
    source_doc = summary_index.docstore.get_document("test_id_1", raise_error=False)
    assert source_doc is None

    summary_index = SummaryIndex.from_documents(
        new_documents, service_context=mock_service_context
    )
    summary_index.delete_ref_doc("test_id_2")
    assert len(summary_index.index_struct.nodes) == 3
    nodes = summary_index.docstore.get_nodes(summary_index.index_struct.nodes)
    assert nodes[0].ref_doc_id == "test_id_1"
    assert nodes[0].get_content() == "Hello world."
    assert nodes[1].ref_doc_id == "test_id_1"
    assert nodes[1].get_content() == "This is a test."
    assert nodes[2].ref_doc_id == "test_id_3"
    assert nodes[2].get_content() == "This is a test v2."

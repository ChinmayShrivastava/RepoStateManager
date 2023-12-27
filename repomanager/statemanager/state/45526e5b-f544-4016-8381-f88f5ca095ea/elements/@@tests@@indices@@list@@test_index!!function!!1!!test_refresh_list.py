def test_refresh_list(
    documents: List[Document],
    mock_service_context: ServiceContext,
) -> None:
    """Test build list."""
    # add extra document
    more_documents = [*documents, Document(text="Test document 2")]

    # ensure documents have doc_id
    for i in range(len(more_documents)):
        more_documents[i].doc_id = str(i)  # type: ignore[misc]

    # create index
    summary_index = SummaryIndex.from_documents(
        more_documents, service_context=mock_service_context
    )

    # check that no documents are refreshed
    refreshed_docs = summary_index.refresh_ref_docs(more_documents)
    assert refreshed_docs[0] is False
    assert refreshed_docs[1] is False

    # modify a document and test again
    more_documents = [*documents, Document(text="Test document 2, now with changes!")]
    for i in range(len(more_documents)):
        more_documents[i].doc_id = str(i)  # type: ignore[misc]

    # second document should refresh
    refreshed_docs = summary_index.refresh_ref_docs(more_documents)
    assert refreshed_docs[0] is False
    assert refreshed_docs[1] is True

    test_node = summary_index.docstore.get_node(summary_index.index_struct.nodes[-1])
    assert test_node.get_content() == "Test document 2, now with changes!"

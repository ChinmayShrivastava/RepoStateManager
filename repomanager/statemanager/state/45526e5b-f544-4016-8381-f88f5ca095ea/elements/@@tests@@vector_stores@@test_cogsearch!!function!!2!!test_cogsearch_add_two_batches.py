def test_cogsearch_add_two_batches() -> None:
    search_client = MagicMock(spec=SearchClient)
    vector_store = create_mock_vector_store(search_client)

    nodes = create_sample_documents(11)

    ids = vector_store.add(nodes)

    call_count = search_client.merge_or_upload_documents.call_count

    assert ids is not None
    assert len(ids) == 11
    assert call_count == 2

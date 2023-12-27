def test_cogsearch_add_one_batch() -> None:
    search_client = MagicMock(spec=SearchClient)
    vector_store = create_mock_vector_store(search_client)

    nodes = create_sample_documents(10)

    ids = vector_store.add(nodes)

    call_count = search_client.merge_or_upload_documents.call_count

    assert ids is not None
    assert len(ids) == 10
    assert call_count == 1

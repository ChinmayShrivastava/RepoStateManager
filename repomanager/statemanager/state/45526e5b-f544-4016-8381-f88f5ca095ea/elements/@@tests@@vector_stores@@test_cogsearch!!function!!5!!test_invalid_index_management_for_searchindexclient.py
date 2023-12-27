def test_invalid_index_management_for_searchindexclient() -> None:
    search_client = MagicMock(spec=SearchIndexClient)

    # Index name must be supplied
    with pytest.raises(ValueError):
        create_mock_vector_store(
            search_client, index_management=IndexManagement.VALIDATE_INDEX
        )

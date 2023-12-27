def test_invalid_index_management_for_searchclient() -> None:
    search_client = MagicMock(spec=SearchClient)

    # No error
    create_mock_vector_store(
        search_client, index_management=IndexManagement.VALIDATE_INDEX
    )

    # Cannot supply index name
    # ruff: noqa: E501
    with pytest.raises(
        ValueError,
        match="index_name cannot be supplied if search_or_index_client is of type azure.search.documents.SearchClient",
    ):
        create_mock_vector_store(search_client, index_name="test01")

    # SearchClient cannot create an index
    with pytest.raises(ValueError):
        create_mock_vector_store(
            search_client,
            index_management=IndexManagement.CREATE_IF_NOT_EXISTS,
        )

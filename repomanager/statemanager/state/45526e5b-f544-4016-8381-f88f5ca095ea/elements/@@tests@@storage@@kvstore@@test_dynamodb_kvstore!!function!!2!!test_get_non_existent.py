def test_get_non_existent(kvstore_from_mocked_table: DynamoDBKVStore) -> None:
    test_key = "test_key"
    item = kvstore_from_mocked_table.get(key=test_key)
    assert item is None

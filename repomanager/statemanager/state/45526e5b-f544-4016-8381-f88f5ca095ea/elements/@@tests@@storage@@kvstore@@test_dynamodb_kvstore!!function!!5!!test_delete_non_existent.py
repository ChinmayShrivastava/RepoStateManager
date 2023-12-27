def test_delete_non_existent(kvstore_from_mocked_table: DynamoDBKVStore) -> None:
    test_key = "test_key"
    test_item = {"test_item_key": "test_item_val"}
    kvstore_from_mocked_table.put(key=test_key, val=test_item)
    assert kvstore_from_mocked_table.delete(key="wrong_key") is False

def test_delete(kvstore_from_mocked_table: DynamoDBKVStore) -> None:
    test_key = "test_key"
    test_item = {"test_item": "test_item_val"}
    kvstore_from_mocked_table.put(key=test_key, val=test_item)
    item = kvstore_from_mocked_table.get(key=test_key)
    assert item == test_item
    assert kvstore_from_mocked_table.delete(key=test_key)

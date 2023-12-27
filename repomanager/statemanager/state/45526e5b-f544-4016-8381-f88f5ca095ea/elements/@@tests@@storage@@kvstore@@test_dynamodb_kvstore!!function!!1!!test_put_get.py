def test_put_get(kvstore_from_mocked_table: DynamoDBKVStore) -> None:
    test_key = "test_key"
    test_value = {"test_str": "test_str", "test_float": 3.14}
    kvstore_from_mocked_table.put(key=test_key, val=test_value)
    item = kvstore_from_mocked_table.get(key=test_key)
    assert item == test_value

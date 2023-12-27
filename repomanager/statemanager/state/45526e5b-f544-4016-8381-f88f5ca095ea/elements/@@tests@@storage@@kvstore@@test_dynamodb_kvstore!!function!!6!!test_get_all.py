def test_get_all(kvstore_from_mocked_table: DynamoDBKVStore) -> None:
    test_key_a = "test_key_a"
    test_item_a = {"test_item_key": "test_item_val_a"}

    test_key_b = "test_key_b"
    test_item_b = {"test_item_key": "test_item_val_b"}

    kvstore_from_mocked_table.put(key=test_key_a, val=test_item_a)
    kvstore_from_mocked_table.put(key=test_key_b, val=test_item_b)

    items = kvstore_from_mocked_table.get_all()
    assert items == {test_key_a: test_item_a, test_key_b: test_item_b}

def test_put_get_multiple_collections(
    kvstore_from_mocked_table: DynamoDBKVStore,
) -> None:
    test_key = "test_key"
    test_item_collection_a = {"test_obj_key": "a"}
    test_item_collection_b = {"test_obj_key": "b"}
    kvstore_from_mocked_table.put(
        key=test_key, val=test_item_collection_a, collection="test_collection_a"
    )
    kvstore_from_mocked_table.put(
        key=test_key, val=test_item_collection_b, collection="test_collection_b"
    )
    item_collection_a = kvstore_from_mocked_table.get(
        key=test_key, collection="test_collection_a"
    )
    item_collection_b = kvstore_from_mocked_table.get(
        key=test_key, collection="test_collection_b"
    )
    assert test_item_collection_a == item_collection_a
    assert test_item_collection_b == item_collection_b

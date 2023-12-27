def test_put_get_multiple_collections(kvstore_from_mocked_bucket: S3DBKVStore) -> None:
    test_key = "test_key"
    test_blob_collection_a = {"test_obj_key": "a"}
    test_blob_collection_b = {"test_obj_key": "b"}
    kvstore_from_mocked_bucket.put(
        test_key, test_blob_collection_a, collection="test_collection_a"
    )
    kvstore_from_mocked_bucket.put(
        test_key, test_blob_collection_b, collection="test_collection_b"
    )
    blob_collection_a = kvstore_from_mocked_bucket.get(
        test_key, collection="test_collection_a"
    )
    blob_collection_b = kvstore_from_mocked_bucket.get(
        test_key, collection="test_collection_b"
    )
    assert test_blob_collection_a == blob_collection_a
    assert test_blob_collection_b == blob_collection_b

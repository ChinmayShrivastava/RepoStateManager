def test_delete(kvstore_from_mocked_bucket: S3DBKVStore) -> None:
    test_key = "test_key"
    test_blob = {"test_obj_key": "test_obj_val"}
    kvstore_from_mocked_bucket.put(test_key, test_blob)
    blob = kvstore_from_mocked_bucket.get(test_key)
    assert blob == test_blob
    assert kvstore_from_mocked_bucket.delete(test_key)

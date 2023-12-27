def test_get_all(kvstore_from_mocked_bucket: S3DBKVStore) -> None:
    test_key_a = "test_key_a"
    test_blob_a = {"test_obj_key": "test_obj_val_a"}

    test_key_b = "test_key_b"
    test_blob_b = {"test_obj_key": "test_obj_val_b"}
    kvstore_from_mocked_bucket.put(test_key_a, test_blob_a)
    kvstore_from_mocked_bucket.put(test_key_b, test_blob_b)
    blobs = kvstore_from_mocked_bucket.get_all()

    assert blobs == {test_key_a: test_blob_a, test_key_b: test_blob_b}

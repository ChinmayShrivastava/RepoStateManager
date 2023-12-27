def test_delete_non_existent(kvstore_from_mocked_bucket: S3DBKVStore) -> None:
    test_key = "test_key"
    test_blob = {"test_obj_key": "test_obj_val"}
    kvstore_from_mocked_bucket.put(test_key, test_blob)
    assert kvstore_from_mocked_bucket.delete("wrong_key") is False

def test_get_non_existent(kvstore_from_mocked_bucket: S3DBKVStore) -> None:
    test_key = "test_key"
    blob = kvstore_from_mocked_bucket.get(test_key)
    assert blob is None

def kvstore_with_data(simple_kvstore: SimpleKVStore) -> SimpleKVStore:
    test_key = "test_key"
    test_blob = {"test_obj_key": "test_obj_val"}
    simple_kvstore.put(test_key, test_blob)
    return simple_kvstore

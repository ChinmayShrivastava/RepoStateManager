def kvstore_with_data(mongo_kvstore: MongoDBKVStore) -> MongoDBKVStore:
    test_key = "test_key"
    test_blob = {"test_obj_key": "test_obj_val"}
    mongo_kvstore.put(test_key, test_blob)
    return mongo_kvstore

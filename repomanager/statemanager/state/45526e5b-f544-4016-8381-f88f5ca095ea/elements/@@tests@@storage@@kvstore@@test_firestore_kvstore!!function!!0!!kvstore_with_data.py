def kvstore_with_data(firestore_kvstore: FirestoreKVStore) -> FirestoreKVStore:
    test_key = "test_key"
    test_doc = {"test_obj_key": "test_obj_val"}
    firestore_kvstore.put(test_key, test_doc)
    return firestore_kvstore

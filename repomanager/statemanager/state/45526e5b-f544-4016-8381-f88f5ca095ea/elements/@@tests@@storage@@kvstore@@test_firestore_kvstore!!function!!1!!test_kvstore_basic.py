def test_kvstore_basic(firestore_kvstore: FirestoreKVStore) -> None:
    test_key = "test_key"
    test_doc = {"test_obj_key": "test_obj_val"}
    firestore_kvstore.put(test_key, test_doc)
    doc = firestore_kvstore.get(test_key)
    assert doc == test_doc

    doc = firestore_kvstore.get(test_key, collection="non_existent")
    assert doc is None

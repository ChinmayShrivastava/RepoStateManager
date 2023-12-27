def test_firestore_docstore(firestore_indexstore: FirestoreIndexStore) -> None:
    index_struct = IndexGraph()
    index_store = firestore_indexstore

    index_store.add_index_struct(index_struct)
    assert index_store.get_index_struct(struct_id=index_struct.index_id) == index_struct

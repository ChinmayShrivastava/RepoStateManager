def firestore_indexstore(firestore_kvstore: FirestoreKVStore) -> FirestoreIndexStore:
    return FirestoreIndexStore(firestore_kvstore=firestore_kvstore)

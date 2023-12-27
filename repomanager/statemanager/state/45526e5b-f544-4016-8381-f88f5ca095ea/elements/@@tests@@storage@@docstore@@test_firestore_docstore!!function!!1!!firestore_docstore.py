def firestore_docstore(firestore_kvstore: FirestoreKVStore) -> FirestoreDocumentStore:
    return FirestoreDocumentStore(firestore_kvstore=firestore_kvstore)

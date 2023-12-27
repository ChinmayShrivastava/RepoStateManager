def mongodb_docstore(mongo_kvstore: MongoDBKVStore) -> MongoDocumentStore:
    return MongoDocumentStore(mongo_kvstore=mongo_kvstore)

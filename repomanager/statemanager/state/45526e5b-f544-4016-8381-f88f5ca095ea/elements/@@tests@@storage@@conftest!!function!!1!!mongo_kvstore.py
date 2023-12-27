def mongo_kvstore(mongo_client: MockMongoClient) -> MongoDBKVStore:
    return MongoDBKVStore(mongo_client=mongo_client)  # type: ignore

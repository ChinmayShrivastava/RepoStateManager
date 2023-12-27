def ddb_index_store(kvstore_from_mocked_table: DynamoDBKVStore) -> DynamoDBIndexStore:
    return DynamoDBIndexStore(dynamodb_kvstore=kvstore_from_mocked_table)

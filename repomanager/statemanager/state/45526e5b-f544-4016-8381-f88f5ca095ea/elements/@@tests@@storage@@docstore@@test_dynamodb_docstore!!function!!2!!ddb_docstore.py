def ddb_docstore(kvstore_from_mocked_table: DynamoDBKVStore) -> DynamoDBDocumentStore:
    return DynamoDBDocumentStore(dynamodb_kvstore=kvstore_from_mocked_table)

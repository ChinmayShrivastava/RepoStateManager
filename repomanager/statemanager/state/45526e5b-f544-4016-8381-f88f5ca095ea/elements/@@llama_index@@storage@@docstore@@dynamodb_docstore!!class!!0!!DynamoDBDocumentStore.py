class DynamoDBDocumentStore(KVDocumentStore):
    def __init__(
        self, dynamodb_kvstore: DynamoDBKVStore, namespace: str | None = None
    ) -> None:
        super().__init__(kvstore=dynamodb_kvstore, namespace=namespace)

    @classmethod
    def from_table_name(
        cls, table_name: str, namespace: str | None = None
    ) -> DynamoDBDocumentStore:
        dynamodb_kvstore = DynamoDBKVStore.from_table_name(table_name=table_name)
        return cls(dynamodb_kvstore=dynamodb_kvstore, namespace=namespace)

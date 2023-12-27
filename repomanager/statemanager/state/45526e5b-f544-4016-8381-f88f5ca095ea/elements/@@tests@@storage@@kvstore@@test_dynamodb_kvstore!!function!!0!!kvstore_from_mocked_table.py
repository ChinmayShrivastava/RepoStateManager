def kvstore_from_mocked_table(
    monkeypatch: MonkeyPatch,
) -> Generator[DynamoDBKVStore, None, None]:
    monkeypatch.setenv("MOTO_ALLOW_NONEXISTENT_REGION", "True")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "Andes")

    table_name = "test_table"
    with mock_dynamodb():
        client = boto3.client("dynamodb")
        client.create_table(
            TableName=table_name,
            AttributeDefinitions=[
                {"AttributeName": "collection", "AttributeType": "S"},
                {"AttributeName": "key", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "collection", "KeyType": "HASH"},
                {"AttributeName": "key", "KeyType": "RANGE"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        yield DynamoDBKVStore.from_table_name(table_name)

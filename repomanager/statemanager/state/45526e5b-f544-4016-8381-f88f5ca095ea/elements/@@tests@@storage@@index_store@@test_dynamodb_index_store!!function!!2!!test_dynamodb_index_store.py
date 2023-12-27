def test_dynamodb_index_store(ddb_index_store: DynamoDBIndexStore) -> None:
    index_store = ddb_index_store

    index_struct = IndexGraph()
    index_store.add_index_struct(index_struct=index_struct)

    assert index_store.get_index_struct(struct_id=index_struct.index_id) == index_struct

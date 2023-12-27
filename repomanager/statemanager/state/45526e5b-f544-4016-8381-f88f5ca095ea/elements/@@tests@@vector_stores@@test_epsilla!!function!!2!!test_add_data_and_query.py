def test_add_data_and_query() -> None:
    client = vectordb.Client()
    vector_store = EpsillaVectorStore(client=client, collection_name="test_collection")

    assert vector_store._collection_name == "test_collection"
    assert vector_store._collection_created is not True

    nodes = node_embeddings()
    ids = vector_store.add(nodes)

    assert vector_store._collection_created is True
    assert ids is ["1", "2"]

    query = VectorStoreQuery(query_embedding=[1.0, 0.0], similarity_top_k=1)
    query_result = vector_store.query(query)

    assert query_result.ids is ["1"]

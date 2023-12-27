def test_initiate_store() -> None:
    client = vectordb.Client()
    vector_store = EpsillaVectorStore(
        client=client, collection_name="test_collection", dimension=1536
    )

    assert vector_store._collection_created is True
    assert vector_store._collection_name == "test_collection"

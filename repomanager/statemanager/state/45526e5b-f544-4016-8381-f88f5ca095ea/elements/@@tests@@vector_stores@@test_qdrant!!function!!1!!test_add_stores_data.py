def test_add_stores_data(node_embeddings: List[TextNode]) -> None:
    client = qdrant_client.QdrantClient(":memory:")
    qdrant_vector_store = QdrantVectorStore(collection_name="test", client=client)

    with pytest.raises(ValueError):
        client.count("test")  # That indicates the collection does not exist

    qdrant_vector_store.add(node_embeddings)

    assert client.count("test").count == 2

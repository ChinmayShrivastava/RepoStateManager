def test_add_stores_data(node_embeddings: List[TextNode], embedded_milvus: str) -> None:
    milvus_store = MilvusVectorStore(dim=2, uri=embedded_milvus, collection_name="test")

    milvus_store.add(node_embeddings)
    milvus_store.milvusclient.flush("test")
    assert milvus_store.client.num_entities("test") == 2

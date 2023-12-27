def test_query(vector_store: SingleStoreVectorStore) -> None:
    result = vector_store.query(
        VectorStoreQuery(query_embedding=[0.9, 0.1], similarity_top_k=1)
    )
    assert result.nodes is not None
    assert len(result.nodes) == 1
    assert isinstance(result.nodes[0], TextNode)
    assert result.nodes[0].text == "Apples are blue"
    assert result.nodes[0].metadata["type"] == "fruit"

def test_query_with_filter(node_embeddings: List[TextNode]) -> None:
    store = get_tencent_vdb_store()

    query = VectorStoreQuery(
        query_embedding=[0.21, 0.22],
        similarity_top_k=10,
    )

    result = store.query(query, filter="age > 20 and age < 40")
    assert result.nodes is not None
    assert len(result.nodes) == 2
    assert result.nodes[0].metadata.get("author") == "Chris"
    assert result.nodes[1].metadata.get("author") == "Kiwi"

def test_query() -> None:
    store = get_tencent_vdb_store()
    query = VectorStoreQuery(
        query_embedding=[0.21, 0.22],
        similarity_top_k=10,
    )
    result = store.query(query, filter='doc_id in ("test-doc-2", "test-doc-3")')
    assert result.nodes is not None
    assert len(result.nodes) == 2
    assert result.nodes[0].node_id == "38500E76-5436-44A0-9C47-F86AAD56234D"

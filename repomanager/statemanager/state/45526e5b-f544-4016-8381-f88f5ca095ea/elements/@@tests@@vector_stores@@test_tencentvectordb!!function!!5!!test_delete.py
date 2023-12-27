def test_delete(node_embeddings: List[TextNode]) -> None:
    ids = [node_embedding.node_id for node_embedding in node_embeddings]

    store = get_tencent_vdb_store()
    results = store.query_by_ids(ids)
    assert len(results) == 3

    store.delete("test-doc-1")
    time.sleep(2)

    results = store.query_by_ids(ids)
    assert len(results) == 2

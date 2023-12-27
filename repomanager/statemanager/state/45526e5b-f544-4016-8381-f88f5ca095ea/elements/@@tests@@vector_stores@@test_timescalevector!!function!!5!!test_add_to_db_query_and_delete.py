def test_add_to_db_query_and_delete(
    tvs: TimescaleVectorStore, node_embeddings: List[TextNode]
) -> None:
    tvs.add(node_embeddings)
    assert isinstance(tvs, TimescaleVectorStore)

    q = VectorStoreQuery(query_embedding=[0.1] * 1536, similarity_top_k=1)
    res = tvs.query(q)
    assert res.nodes
    assert len(res.nodes) == 1
    assert res.nodes[0].node_id == "bbb"

    tvs.create_index()
    tvs.drop_index()

    tvs.create_index(IndexType.TIMESCALE_VECTOR, max_alpha=1.0, num_neighbors=50)
    tvs.drop_index()

    tvs.create_index(IndexType.PGVECTOR_IVFFLAT, num_lists=20, num_records=1000)
    tvs.drop_index()

    tvs.create_index(IndexType.PGVECTOR_HNSW, m=16, ef_construction=64)
    tvs.drop_index()

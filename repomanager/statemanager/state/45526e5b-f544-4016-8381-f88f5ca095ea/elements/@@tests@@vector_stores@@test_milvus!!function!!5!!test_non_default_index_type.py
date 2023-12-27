def test_non_default_index_type(
    node_embeddings: List[TextNode], embedded_milvus: str
) -> None:
    milvus_store = MilvusVectorStore(
        dim=2,
        uri=embedded_milvus,
        collection_name="test",
        similarity_metric="L2",
        index_config={"index_type": "IVF_FLAT", "nlist": 64},
        search_config={"nprobe": 16},
    )
    milvus_store.add(node_embeddings)

    res = milvus_store.query(
        VectorStoreQuery(query_embedding=[3, 3], similarity_top_k=1)
    )
    assert res.ids is not None and res.ids[0] == "c3d1e1dd-8fb4-4b8f-b7ea-7fa96038d39d"
    assert res.nodes is not None and res.nodes[0].metadata["theme"] == "Mafia"
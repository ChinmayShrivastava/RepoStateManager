def test_search_data_filter(
    node_embeddings: List[TextNode], embedded_milvus: str
) -> None:
    milvus_store = MilvusVectorStore(dim=2, uri=embedded_milvus, collection_name="test")
    milvus_store.add(node_embeddings)

    res = milvus_store.query(
        VectorStoreQuery(
            query_embedding=[3, 3],
            similarity_top_k=1,
            filters=MetadataFilters(
                filters=[ExactMatchFilter(key="theme", value="Friendship")]
            ),
        )
    )

    assert res.ids is not None and res.ids[0] == "c330d77f-90bd-4c51-9ed2-57d8d693b3b0"
    assert res.nodes is not None and res.nodes[0].metadata["theme"] == "Friendship"

    print(node_embeddings[0].node_id)
    res = milvus_store.query(
        VectorStoreQuery(
            query_embedding=[3, 3],
            node_ids=["c330d77f-90bd-4c51-9ed2-57d8d693b3b0"],
            similarity_top_k=1,
        )
    )
    assert res.ids is not None and res.ids[0] == "c330d77f-90bd-4c51-9ed2-57d8d693b3b0"
    assert res.nodes is not None and res.nodes[0].metadata["theme"] == "Friendship"

    res = milvus_store.query(
        VectorStoreQuery(
            query_embedding=[3, 3],
            doc_ids=["test-0"],
            similarity_top_k=1,
        )
    )
    assert res.ids is not None and res.ids[0] == "c330d77f-90bd-4c51-9ed2-57d8d693b3b0"
    assert res.nodes is not None and res.nodes[0].metadata["theme"] == "Friendship"

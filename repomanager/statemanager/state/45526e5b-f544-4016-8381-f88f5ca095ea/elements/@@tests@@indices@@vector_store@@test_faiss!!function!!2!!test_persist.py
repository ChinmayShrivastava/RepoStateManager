def test_persist(tmp_path: Path) -> None:
    import faiss

    vector_store = FaissVectorStore(faiss_index=faiss.IndexFlatL2(5))

    vector_store.add(
        [
            TextNode(
                text="test text",
                embedding=[0, 0, 0, 1, 1],
            ),
        ]
    )

    result = vector_store.query(VectorStoreQuery(query_embedding=[0, 0, 0, 1, 1]))

    persist_path = str(tmp_path / "faiss.index")
    vector_store.persist(persist_path)
    new_vector_store = FaissVectorStore.from_persist_path(persist_path)
    new_result = new_vector_store.query(
        VectorStoreQuery(query_embedding=[0, 0, 0, 1, 1])
    )

    assert result == new_result

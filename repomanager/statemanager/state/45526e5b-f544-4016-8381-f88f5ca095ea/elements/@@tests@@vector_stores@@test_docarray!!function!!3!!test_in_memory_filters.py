def test_in_memory_filters(node_embeddings: List[TextNode]) -> None:
    docarray_vector_store = DocArrayInMemoryVectorStore()
    docarray_vector_store.add(node_embeddings)
    assert docarray_vector_store.num_docs() == 3

    filters = MetadataFilters(filters=[ExactMatchFilter(key="theme", value="Mafia")])

    query_emb = VectorStoreQuery(query_embedding=[0.0, 0.1, 0.0], filters=filters)
    res = docarray_vector_store.query(query_emb)

    assert res.nodes is not None
    assert len(res.nodes) == 1  # type: ignore[arg-type]
    assert res.nodes[0].metadata["theme"] == "Mafia"  # type: ignore[index]
    rf = res.nodes[0].ref_doc_id
    assert rf == "test-1"

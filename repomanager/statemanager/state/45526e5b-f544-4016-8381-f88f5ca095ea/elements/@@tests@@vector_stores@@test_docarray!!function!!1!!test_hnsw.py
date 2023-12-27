def test_hnsw(node_embeddings: List[TextNode], tmp_path: Path) -> None:
    docarray_vector_store = DocArrayHnswVectorStore(work_dir=str(tmp_path), dim=3)
    docarray_vector_store.add(node_embeddings)
    assert docarray_vector_store.num_docs() == 3

    query_emb = VectorStoreQuery(query_embedding=[0.0, 0.1, 0.0])
    res = docarray_vector_store.query(query_emb)

    assert res.nodes is not None
    assert len(res.nodes) == 1  # type: ignore[arg-type]
    rf = res.nodes[0].ref_doc_id
    assert rf == "test-1"

    docarray_vector_store.delete(ref_doc_id="test-1")
    assert docarray_vector_store.num_docs() == 2

    new_vector_store = DocArrayHnswVectorStore(work_dir=str(tmp_path), dim=3)
    assert new_vector_store.num_docs() == 2

    new_vector_store.delete(ref_doc_id="test-0")
    assert new_vector_store.num_docs() == 1

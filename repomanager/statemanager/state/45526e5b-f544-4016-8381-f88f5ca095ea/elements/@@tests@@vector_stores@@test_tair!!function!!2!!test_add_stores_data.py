def test_add_stores_data(node_embeddings: List[TextNode]) -> None:
    tair_url = get_tair_url()
    tair_vector_store = TairVectorStore(tair_url=tair_url, index_name="test_index")

    tair_vector_store.add(node_embeddings)

    info = tair_vector_store.client.tvs_get_index("test_index")
    assert int(info["data_count"]) == 3

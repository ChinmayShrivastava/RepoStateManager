def test_delete() -> None:
    tair_url = get_tair_url()
    tair_vector_store = TairVectorStore(tair_url=tair_url, index_name="test_index")

    tair_vector_store.delete("test-1")
    info = tair_vector_store.client.tvs_get_index("test_index")
    assert int(info["data_count"]) == 1

    query = VectorStoreQuery(query_embedding=[1.0, 1.0])
    result = tair_vector_store.query(query)
    assert (
        result.ids is not None
        and len(result.ids) == 1
        and result.ids[0] == "AF3BE6C4-5F43-4D74-B075-6B0E07900DE8"
    )

    tair_vector_store.delete_index()
    info = tair_vector_store.client.tvs_get_index("test_index")
    assert info is None

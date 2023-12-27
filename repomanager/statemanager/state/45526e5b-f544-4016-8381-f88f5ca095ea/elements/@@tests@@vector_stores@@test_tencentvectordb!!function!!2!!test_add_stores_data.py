def test_add_stores_data(node_embeddings: List[TextNode]) -> None:
    store = get_tencent_vdb_store(drop_exists=True)
    store.add(node_embeddings)
    time.sleep(2)

    results = store.query_by_ids(
        ["31BA2AA7-E066-452D-B0A6-0935FACE94FC", "38500E76-5436-44A0-9C47-F86AAD56234D"]
    )
    assert len(results) == 2

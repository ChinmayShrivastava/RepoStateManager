def test_cache() -> None:
    cache = IngestionCache()
    transformation = DummyTransform()

    node = TextNode(text="dummy")
    hash = get_transformation_hash([node], transformation)

    new_nodes = transformation([node])
    cache.put(hash, new_nodes)

    cache_hit = cache.get(hash)
    assert cache_hit is not None
    assert cache_hit[0].get_content() == new_nodes[0].get_content()

    new_hash = get_transformation_hash(new_nodes, transformation)
    assert cache.get(new_hash) is None

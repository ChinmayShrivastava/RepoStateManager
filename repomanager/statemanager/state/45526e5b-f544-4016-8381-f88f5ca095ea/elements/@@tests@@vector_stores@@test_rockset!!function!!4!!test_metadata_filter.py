def test_metadata_filter(vector_store: RocksetVectorStore) -> None:
    result = vector_store.query(
        VectorStoreQuery(
            filters=MetadataFilters(
                filters=[ExactMatchFilter(key="type", value="dessert")]
            )
        )
    )
    assert result.nodes is not None
    assert len(result.nodes) == 1
    assert isinstance(result.nodes[0], TextNode)
    assert result.nodes[0].text == "Brownies are orange"
    assert result.nodes[0].metadata["type"] == "dessert"

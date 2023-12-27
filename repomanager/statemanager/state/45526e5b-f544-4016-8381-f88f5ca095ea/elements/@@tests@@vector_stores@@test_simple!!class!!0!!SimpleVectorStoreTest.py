class SimpleVectorStoreTest(unittest.TestCase):
    def test_query_without_filters_returns_all_rows_sorted_by_similarity(self) -> None:
        simple_vector_store = SimpleVectorStore()
        simple_vector_store.add(_node_embeddings_for_test())

        query = VectorStoreQuery(query_embedding=[1.0, 1.0], similarity_top_k=3)
        result = simple_vector_store.query(query)
        assert result.ids is not None
        self.assertCountEqual(
            result.ids,
            [
                _NODE_ID_WEIGHT_1_RANK_A,
                _NODE_ID_WEIGHT_2_RANK_C,
                _NODE_ID_WEIGHT_3_RANK_C,
            ],
        )
        self.assertEqual(result.ids[0], _NODE_ID_WEIGHT_3_RANK_C)

    def test_query_with_filters_returns_multiple_matches(self) -> None:
        simple_vector_store = SimpleVectorStore()
        simple_vector_store.add(_node_embeddings_for_test())

        filters = MetadataFilters(filters=[ExactMatchFilter(key="rank", value="c")])
        query = VectorStoreQuery(
            query_embedding=[1.0, 1.0], filters=filters, similarity_top_k=3
        )
        result = simple_vector_store.query(query)
        self.assertEqual(
            result.ids, [_NODE_ID_WEIGHT_3_RANK_C, _NODE_ID_WEIGHT_2_RANK_C]
        )

    def test_query_with_filter_applies_top_k(self) -> None:
        simple_vector_store = SimpleVectorStore()
        simple_vector_store.add(_node_embeddings_for_test())

        filters = MetadataFilters(filters=[ExactMatchFilter(key="rank", value="c")])
        query = VectorStoreQuery(
            query_embedding=[1.0, 1.0], filters=filters, similarity_top_k=1
        )
        result = simple_vector_store.query(query)
        self.assertEqual(result.ids, [_NODE_ID_WEIGHT_3_RANK_C])

    def test_query_with_filter_applies_node_id_filter(self) -> None:
        simple_vector_store = SimpleVectorStore()
        simple_vector_store.add(_node_embeddings_for_test())

        filters = MetadataFilters(filters=[ExactMatchFilter(key="rank", value="c")])
        query = VectorStoreQuery(
            query_embedding=[1.0, 1.0],
            filters=filters,
            similarity_top_k=3,
            node_ids=[_NODE_ID_WEIGHT_3_RANK_C],
        )
        result = simple_vector_store.query(query)
        self.assertEqual(result.ids, [_NODE_ID_WEIGHT_3_RANK_C])

    def test_query_with_exact_filters_returns_single_match(self) -> None:
        simple_vector_store = SimpleVectorStore()
        simple_vector_store.add(_node_embeddings_for_test())

        filters = MetadataFilters(
            filters=[
                ExactMatchFilter(key="rank", value="c"),
                ExactMatchFilter(key="weight", value=2.0),
            ]
        )
        query = VectorStoreQuery(query_embedding=[1.0, 1.0], filters=filters)
        result = simple_vector_store.query(query)
        self.assertEqual(result.ids, [_NODE_ID_WEIGHT_2_RANK_C])

    def test_query_with_contradictive_filter_returns_no_matches(self) -> None:
        simple_vector_store = SimpleVectorStore()
        simple_vector_store.add(_node_embeddings_for_test())

        filters = MetadataFilters(
            filters=[
                ExactMatchFilter(key="weight", value=2),
                ExactMatchFilter(key="weight", value=3),
            ]
        )
        query = VectorStoreQuery(query_embedding=[1.0, 1.0], filters=filters)
        result = simple_vector_store.query(query)
        assert result.ids is not None
        self.assertEqual(len(result.ids), 0)

    def test_query_with_filter_on_unknown_field_returns_no_matches(self) -> None:
        simple_vector_store = SimpleVectorStore()
        simple_vector_store.add(_node_embeddings_for_test())

        filters = MetadataFilters(
            filters=[ExactMatchFilter(key="unknown_field", value="c")]
        )
        query = VectorStoreQuery(query_embedding=[1.0, 1.0], filters=filters)
        result = simple_vector_store.query(query)
        assert result.ids is not None
        self.assertEqual(len(result.ids), 0)

    def test_delete_removes_document_from_query_results(self) -> None:
        simple_vector_store = SimpleVectorStore()
        simple_vector_store.add(_node_embeddings_for_test())

        simple_vector_store.delete("test-1")
        query = VectorStoreQuery(query_embedding=[1.0, 1.0], similarity_top_k=2)
        result = simple_vector_store.query(query)
        self.assertEqual(
            result.ids,
            [_NODE_ID_WEIGHT_3_RANK_C, _NODE_ID_WEIGHT_1_RANK_A],
        )

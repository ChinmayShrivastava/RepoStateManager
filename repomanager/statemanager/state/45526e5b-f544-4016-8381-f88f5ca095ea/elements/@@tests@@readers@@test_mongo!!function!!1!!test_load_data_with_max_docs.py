def test_load_data_with_max_docs() -> None:
    """Test Mongo reader with max_docs."""
    mock_cursor = [{"text": "one"}, {"text": "two"}, {"text": "three"}]

    with patch("pymongo.collection.Collection.find") as mock_find:

        def limit_fn(limit: int, *_args: Any, **_kwargs: Any) -> List[Dict[str, str]]:
            if limit == 0:
                return mock_cursor
            return mock_cursor[:limit]

        mock_find.side_effect = limit_fn

        reader = SimpleMongoReader("host", 1)
        documents = reader.load_data("my_db", "my_collection", max_docs=2)

        assert len(documents) == 2
        assert documents[0].get_content() == "one"
        assert documents[1].get_content() == "two"

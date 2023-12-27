def test_load_data() -> None:
    """Test Mongo reader using default field_names."""
    mock_cursor = [{"text": "one"}, {"text": "two"}, {"text": "three"}]

    with patch("pymongo.collection.Collection.find") as mock_find:
        mock_find.return_value = mock_cursor

        reader = SimpleMongoReader("host", 1)
        documents = reader.load_data("my_db", "my_collection")

        assert len(documents) == 3
        assert documents[0].get_content() == "one"
        assert documents[1].get_content() == "two"
        assert documents[2].get_content() == "three"

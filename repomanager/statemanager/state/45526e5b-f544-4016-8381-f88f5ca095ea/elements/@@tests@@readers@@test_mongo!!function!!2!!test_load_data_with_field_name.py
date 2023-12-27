def test_load_data_with_field_name() -> None:
    """Test Mongo reader using passed in field_names."""
    mock_cursor = [
        {"first": "first1", "second": ["second1", "second11"], "third": "third1"},
        {"first": "first2", "second": ["second2", "second22"], "third": "third2"},
        {"first": "first3", "second": ["second3", "second33"], "third": "third3"},
    ]

    with patch("pymongo.collection.Collection.find") as mock_find:
        mock_find.return_value = mock_cursor

        reader = SimpleMongoReader("host", 1)
        documents = reader.load_data(
            "my_db", "my_collection", field_names=["first", "second", "third"]
        )

        assert len(documents) == 3
        assert documents[0].get_content() == "first1second1second11third1"
        assert documents[1].get_content() == "first2second2second22third2"
        assert documents[2].get_content() == "first3second3second33third3"

def test_load_data_with_metadata_name() -> None:
    """Test Mongo reader using passed in metadata_name."""
    mock_cursor = [
        {"first": "first1", "second": "second1", "third": "third1"},
        {"first": "first2", "second": "second2", "third": "third2"},
        {"first": "first3", "second": "second3", "third": "third3"},
    ]

    with patch("pymongo.collection.Collection.find") as mock_find:
        mock_find.return_value = mock_cursor

        reader = SimpleMongoReader("host", 1)
        documents = reader.load_data(
            "my_db",
            "my_collection",
            field_names=["first"],
            metadata_names=["second", "third"],
        )

        assert len(documents) == 3
        assert documents[0].get_metadata_str() == "second: second1\nthird: third1"
        assert documents[1].get_metadata_str() == "second: second2\nthird: third2"
        assert documents[2].get_metadata_str() == "second: second3\nthird: third3"
        assert (
            documents[0].get_content(metadata_mode=MetadataMode.ALL)
            == "second: second1\nthird: third1\n\nfirst1"
        )
        assert (
            documents[1].get_content(metadata_mode=MetadataMode.ALL)
            == "second: second2\nthird: third2\n\nfirst2"
        )
        assert (
            documents[2].get_content(metadata_mode=MetadataMode.ALL)
            == "second: second3\nthird: third3\n\nfirst3"
        )

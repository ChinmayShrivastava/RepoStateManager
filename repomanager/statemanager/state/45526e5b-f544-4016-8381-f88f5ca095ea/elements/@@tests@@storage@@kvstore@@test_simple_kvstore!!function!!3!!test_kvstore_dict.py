def test_kvstore_dict(kvstore_with_data: SimpleKVStore) -> None:
    """Test kvstore dict."""
    save_dict = kvstore_with_data.to_dict()
    loaded_kvstore = SimpleKVStore.from_dict(save_dict)
    assert len(loaded_kvstore.get_all()) == 1

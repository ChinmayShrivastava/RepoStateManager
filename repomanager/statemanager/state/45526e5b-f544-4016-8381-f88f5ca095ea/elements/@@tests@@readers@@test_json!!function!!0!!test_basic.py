def test_basic() -> None:
    """Test JSON reader in basic mode."""
    with TemporaryDirectory() as tmp_dir:
        file_name = f"{tmp_dir}/test1.json"

        with open(file_name, "w") as f:
            f.write('{"test1": "test1"}')

        reader = JSONReader()
        data = reader.load_data(file_name)
        assert len(data) == 1
        assert isinstance(data[0].get_content(), str)
        assert data[0].get_content().index("test1") is not None

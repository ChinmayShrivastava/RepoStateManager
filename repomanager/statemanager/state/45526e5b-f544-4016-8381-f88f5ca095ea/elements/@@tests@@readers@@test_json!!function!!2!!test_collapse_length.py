def test_collapse_length() -> None:
    """Test JSON reader using the collapse_length function."""
    with TemporaryDirectory() as tmp_dir:
        file_name = f"{tmp_dir}/test3.json"
        with open(file_name, "w") as f:
            f.write('{ "a": { "b": "c" } }')

        reader1 = JSONReader(levels_back=0, collapse_length=100)
        data1 = reader1.load_data(file_name)
        assert isinstance(data1[0].get_content(), str)
        assert data1[0].get_content().index('"a":') is not None

        reader2 = JSONReader(levels_back=0, collapse_length=10)
        data2 = reader2.load_data(file_name)
        assert isinstance(data2[0].get_content(), str)
        assert data2[0].get_content().index("a ") is not None

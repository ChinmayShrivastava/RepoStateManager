def test_levels_back0() -> None:
    """Test JSON reader using the levels_back function."""
    with TemporaryDirectory() as tmp_dir:
        file_name = f"{tmp_dir}/test2.json"
        with open(file_name, "w") as f:
            f.write('{ "a": { "b": "c" } }')

        reader1 = JSONReader(levels_back=0)
        data1 = reader1.load_data(file_name)
        assert data1[0].get_content() == "a b c"

        reader2 = JSONReader(levels_back=1)
        data2 = reader2.load_data(file_name)
        assert data2[0].get_content() == "b c"

def test_jsonl() -> None:
    """Test JSON reader using the is_jsonl function."""
    with TemporaryDirectory() as tmp_dir:
        file_name = f"{tmp_dir}/test4.json"
        with open(file_name, "w") as f:
            f.write('{"test1": "test1"}\n{"test2": "test2"}\n{"test3": "test3"}\n')

        reader = JSONReader(is_jsonl=True)
        data = reader.load_data(file_name)
        assert len(data) == 3
        assert isinstance(data[0].get_content(), str)
        assert data[0].get_content().index("test1") is not None
        assert isinstance(data[1].get_content(), str)
        assert data[1].get_content().index("test2") is not None
        assert isinstance(data[2].get_content(), str)
        assert data[2].get_content().index("test3") is not None

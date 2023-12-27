def test_error_if_not_dir_or_file() -> None:
    with pytest.raises(ValueError, match="Directory"):
        SimpleDirectoryReader("not_a_dir")
    with pytest.raises(ValueError, match="File"):
        SimpleDirectoryReader(input_files=["not_a_file"])
    with TemporaryDirectory() as tmp_dir, pytest.raises(ValueError, match="No files"):
        SimpleDirectoryReader(tmp_dir)

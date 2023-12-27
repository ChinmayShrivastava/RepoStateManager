def test_required_exts() -> None:
    """Test extension filter."""
    # test nonrecursive
    with TemporaryDirectory() as tmp_dir:
        with open(f"{tmp_dir}/test1.txt", "w") as f:
            f.write("test1")
        with open(f"{tmp_dir}/test2.md", "w") as f:
            f.write("test2")
        with open(f"{tmp_dir}/test3.tmp", "w") as f:
            f.write("test3")
        with open(f"{tmp_dir}/test4.json", "w") as f:
            f.write("test4")
        with open(f"{tmp_dir}/test5.json", "w") as f:
            f.write("test5")

        # test exclude hidden
        reader = SimpleDirectoryReader(tmp_dir, required_exts=[".json"])
        input_file_names = [f.name for f in reader.input_files]
        assert len(reader.input_files) == 2
        assert input_file_names == ["test4.json", "test5.json"]

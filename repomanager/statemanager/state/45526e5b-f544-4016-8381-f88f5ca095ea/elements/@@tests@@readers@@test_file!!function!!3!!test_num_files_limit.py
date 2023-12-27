def test_num_files_limit() -> None:
    """Test num files limit."""
    # test num_files_limit (with recursion)
    with TemporaryDirectory() as tmp_dir:
        with open(f"{tmp_dir}/test1.txt", "w") as f:
            f.write("test1")
        with TemporaryDirectory(dir=tmp_dir) as tmp_sub_dir:
            with open(f"{tmp_sub_dir}/test2.txt", "w") as f:
                f.write("test2")
            with open(f"{tmp_sub_dir}/test3.txt", "w") as f:
                f.write("test3")
            with TemporaryDirectory(dir=tmp_sub_dir) as tmp_sub_sub_dir:
                with open(f"{tmp_sub_sub_dir}/test4.txt", "w") as f:
                    f.write("test4")

                    reader = SimpleDirectoryReader(
                        tmp_dir, recursive=True, num_files_limit=2
                    )
                    input_file_names = [f.name for f in reader.input_files]
                    assert len(reader.input_files) == 2
                    assert set(input_file_names) == {
                        "test1.txt",
                        "test2.txt",
                    }

                    reader = SimpleDirectoryReader(
                        tmp_dir, recursive=True, num_files_limit=3
                    )
                    input_file_names = [f.name for f in reader.input_files]
                    assert len(reader.input_files) == 3
                    assert set(input_file_names) == {
                        "test1.txt",
                        "test2.txt",
                        "test3.txt",
                    }

                    reader = SimpleDirectoryReader(
                        tmp_dir, recursive=True, num_files_limit=4
                    )
                    input_file_names = [f.name for f in reader.input_files]
                    assert len(reader.input_files) == 4
                    assert set(input_file_names) == {
                        "test1.txt",
                        "test2.txt",
                        "test3.txt",
                        "test4.txt",
                    }

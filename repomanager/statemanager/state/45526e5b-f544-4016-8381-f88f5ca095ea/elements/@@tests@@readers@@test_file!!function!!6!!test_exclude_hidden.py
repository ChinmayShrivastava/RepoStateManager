def test_exclude_hidden() -> None:
    """Test if exclude_hidden flag excludes hidden files and files in hidden directories."""
    # test recursive exclude hidden
    with TemporaryDirectory() as tmp_dir:
        with open(f"{tmp_dir}/test1.txt", "w") as f:
            f.write("test1")
        with TemporaryDirectory(dir=tmp_dir) as tmp_sub_dir:
            # hidden file
            with open(f"{tmp_sub_dir}/.test2.txt", "w") as f:
                f.write("test2")
            with TemporaryDirectory(dir=tmp_sub_dir) as tmp_sub_sub_a_dir:
                with open(f"{tmp_sub_sub_a_dir}/test3.txt", "w") as f:
                    f.write("test3")
                # hidden directory
                with TemporaryDirectory(
                    dir=tmp_sub_dir, prefix="."
                ) as tmp_sub_sub_b_dir:
                    with open(f"{tmp_sub_sub_b_dir}/test4.txt", "w") as f:
                        f.write("test4")
                    with open(f"{tmp_sub_sub_b_dir}/test5.txt", "w") as f:
                        f.write("test5")

                        reader = SimpleDirectoryReader(
                            tmp_dir, recursive=True, exclude_hidden=True
                        )
                        input_file_names = [f.name for f in reader.input_files]
                        assert len(reader.input_files) == 2
                        assert set(input_file_names) == {"test1.txt", "test3.txt"}

    # test non-recursive exclude hidden files
    with TemporaryDirectory() as tmp_dir:
        with open(f"{tmp_dir}/test1.py", "w") as f:
            f.write("test1.py")
        with open(f"{tmp_dir}/test2.txt", "w") as f:
            f.write("test2")
        with open(f"{tmp_dir}/.test3.txt", "w") as f:
            f.write("test3")
        with open(f"{tmp_dir}/test4.txt", "w") as f:
            f.write("test4")
        with open(f"{tmp_dir}/.test5.py", "w") as f:
            f.write("test5")

        reader = SimpleDirectoryReader(tmp_dir, recursive=False, exclude_hidden=True)
        input_file_names = [f.name for f in reader.input_files]
        assert len(reader.input_files) == 3
        assert input_file_names == ["test1.py", "test2.txt", "test4.txt"]

    # test non-recursive exclude hidden directory
    # - i.e., user passes hidden root directory and tries to use exclude_hidden
    with TemporaryDirectory(prefix=".") as tmp_dir:
        with open(f"{tmp_dir}/test1.py", "w") as f:
            f.write("test1.py")
        with open(f"{tmp_dir}/test2.txt", "w") as f:
            f.write("test2")
        with open(f"{tmp_dir}/.test3.txt", "w") as f:
            f.write("test3")
        with open(f"{tmp_dir}/test4.txt", "w") as f:
            f.write("test4")
        with open(f"{tmp_dir}/.test5.txt", "w") as f:
            f.write("test5")

        # correct behaviour is to raise ValueError as defined in SimpleDirectoryReader._add_files
        try:
            reader = SimpleDirectoryReader(
                tmp_dir, recursive=False, exclude_hidden=True
            )
        except ValueError as e:
            assert e.args[0] == f"No files found in {tmp_dir}."

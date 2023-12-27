def test_excluded_files() -> None:
    """Tests if files are excluded properly."""
    # test recursive
    with TemporaryDirectory() as tmp_dir:
        with open(f"{tmp_dir}/test1.txt", "w") as f:
            f.write("test1")
        with TemporaryDirectory(dir=tmp_dir) as tmp_sub_dir:
            with open(f"{tmp_sub_dir}/test2.txt", "w") as f:
                f.write("test2")
            with TemporaryDirectory(dir=tmp_sub_dir) as tmp_sub_sub_dir:
                with open(f"{tmp_sub_sub_dir}/test3.txt", "w") as f:
                    f.write("test3")
                with open(f"{tmp_sub_sub_dir}/test4.txt", "w") as f:
                    f.write("test4")

                    reader = SimpleDirectoryReader(
                        tmp_dir, recursive=True, exclude=["test3.txt"]
                    )
                    input_file_names = [f.name for f in reader.input_files]
                    assert len(reader.input_files) == 3
                    assert set(input_file_names) == {
                        "test1.txt",
                        "test2.txt",
                        "test4.txt",
                    }

    # test nonrecursive exclude *.py
    with TemporaryDirectory() as tmp_dir:
        with open(f"{tmp_dir}/test1.py", "w") as f:
            f.write("test1.py")
        with open(f"{tmp_dir}/test2.txt", "w") as f:
            f.write("test2")
        with open(f"{tmp_dir}/test3.txt", "w") as f:
            f.write("test3")
        with open(f"{tmp_dir}/test4.txt", "w") as f:
            f.write("test4")
        with open(f"{tmp_dir}/test5.txt", "w") as f:
            f.write("test5")

        reader = SimpleDirectoryReader(tmp_dir, recursive=False, exclude=["*.py"])
        input_file_names = [f.name for f in reader.input_files]
        assert len(reader.input_files) == 4
        assert input_file_names == ["test2.txt", "test3.txt", "test4.txt", "test5.txt"]

    # test recursive exclude *.md
    with TemporaryDirectory() as tmp_dir:
        with open(f"{tmp_dir}/test1.md", "w") as f:
            f.write("test1")
        with TemporaryDirectory(dir=tmp_dir) as tmp_sub_dir:
            with open(f"{tmp_sub_dir}/test2.txt", "w") as f:
                f.write("test2")
            with TemporaryDirectory(dir=tmp_sub_dir) as tmp_sub_sub_dir:
                with open(f"{tmp_sub_sub_dir}/test3.md", "w") as f:
                    f.write("test3")
                with open(f"{tmp_sub_sub_dir}/test4.txt", "w") as f:
                    f.write("test4")

                    reader = SimpleDirectoryReader(
                        tmp_dir, recursive=True, exclude=["*.md"]
                    )
                    input_file_names = [f.name for f in reader.input_files]
                    assert len(reader.input_files) == 2
                    assert set(input_file_names) == {
                        "test2.txt",
                        "test4.txt",
                    }

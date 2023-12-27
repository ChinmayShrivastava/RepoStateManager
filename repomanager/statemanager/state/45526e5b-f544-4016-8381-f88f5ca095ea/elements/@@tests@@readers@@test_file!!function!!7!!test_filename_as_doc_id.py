def test_filename_as_doc_id() -> None:
    """Test if file metadata is added to Document."""
    # test file_metadata
    with TemporaryDirectory() as tmp_dir:
        with open(f"{tmp_dir}/test1.txt", "w") as f:
            f.write("test1")
        with open(f"{tmp_dir}/test2.txt", "w") as f:
            f.write("test2")
        with open(f"{tmp_dir}/test3.txt", "w") as f:
            f.write("test3")
        with open(f"{tmp_dir}/test4.md", "w") as f:
            f.write("test4")
        with open(f"{tmp_dir}/test5.json", "w") as f:
            f.write('{"test_1": {"test_2": [1, 2, 3]}}')

        reader = SimpleDirectoryReader(tmp_dir, filename_as_id=True)

        documents = reader.load_data()

        doc_paths = [
            f"{tmp_dir}/test1.txt",
            f"{tmp_dir}/test2.txt",
            f"{tmp_dir}/test3.txt",
            f"{tmp_dir}/test4.md",
            f"{tmp_dir}/test5.json",
        ]

        # check paths. Split handles path_part_X doc_ids from md and json files
        for doc in documents:
            assert str(doc.node_id).split("_part")[0] in doc_paths

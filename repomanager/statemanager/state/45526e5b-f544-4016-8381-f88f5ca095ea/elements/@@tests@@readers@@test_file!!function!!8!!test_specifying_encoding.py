def test_specifying_encoding() -> None:
    """Test if file metadata is added to Document."""
    # test file_metadata
    with TemporaryDirectory() as tmp_dir:
        with open(f"{tmp_dir}/test1.txt", "w", encoding="latin-1") as f:
            f.write("test1á")
        with open(f"{tmp_dir}/test2.txt", "w", encoding="latin-1") as f:
            f.write("test2â")
        with open(f"{tmp_dir}/test3.txt", "w", encoding="latin-1") as f:
            f.write("test3ã")
        with open(f"{tmp_dir}/test4.json", "w", encoding="latin-1") as f:
            f.write('{"test_1á": {"test_2ã": ["â"]}}')

        reader = SimpleDirectoryReader(
            tmp_dir, filename_as_id=True, errors="strict", encoding="latin-1"
        )

        documents = reader.load_data()

        doc_paths = [
            f"{tmp_dir}/test1.txt",
            f"{tmp_dir}/test2.txt",
            f"{tmp_dir}/test3.txt",
            f"{tmp_dir}/test4.json",
        ]

        # check paths. Split handles path_part_X doc_ids from md and json files
        for doc in documents:
            assert str(doc.node_id).split("_part")[0] in doc_paths

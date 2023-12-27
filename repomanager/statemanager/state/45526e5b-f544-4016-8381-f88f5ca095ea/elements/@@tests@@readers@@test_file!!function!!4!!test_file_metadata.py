def test_file_metadata() -> None:
    """Test if file metadata is added to Document."""
    # test file_metadata
    with TemporaryDirectory() as tmp_dir:
        with open(f"{tmp_dir}/test1.txt", "w") as f:
            f.write("test1")
        with open(f"{tmp_dir}/test2.txt", "w") as f:
            f.write("test2")
        with open(f"{tmp_dir}/test3.txt", "w") as f:
            f.write("test3")

        test_author = "Bruce Wayne"

        def filename_to_metadata(filename: str) -> Dict[str, Any]:
            return {"filename": filename, "author": test_author}

        # test default file_metadata
        reader = SimpleDirectoryReader(tmp_dir)

        documents = reader.load_data()

        for doc in documents:
            assert "file_path" in doc.metadata

        # test customized file_metadata
        reader = SimpleDirectoryReader(tmp_dir, file_metadata=filename_to_metadata)

        documents = reader.load_data()

        for doc in documents:
            assert doc.metadata is not None and doc.metadata["author"] == test_author

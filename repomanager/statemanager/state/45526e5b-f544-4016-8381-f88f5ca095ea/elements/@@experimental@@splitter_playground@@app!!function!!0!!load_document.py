def load_document(uploaded_files: List[UploadedFile]) -> List[Document]:
    # Read documents
    temp_dir = tempfile.TemporaryDirectory()
    for file in uploaded_files:
        temp_filepath = os.path.join(temp_dir.name, file.name)
        with open(temp_filepath, "wb") as f:
            f.write(file.getvalue())

    reader = SimpleDirectoryReader(input_dir=temp_dir.name)
    return reader.load_data()

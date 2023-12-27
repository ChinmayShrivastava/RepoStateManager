def faiss_vector_store(tmp_path: pathlib.Path) -> FaissVectorStore:
    # NOTE: mock faiss import for CI
    if "CI" in os.environ:
        sys.modules["faiss"] = MagicMock()

    # NOTE: mock faiss index
    faiss_index = MockFaissIndex()

    return FaissVectorStore(faiss_index=faiss_index)

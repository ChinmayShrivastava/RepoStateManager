def get_pinecone_storage_context() -> StorageContext:
    # NOTE: mock pinecone import
    sys.modules["pinecone"] = MagicMock()
    return StorageContext.from_defaults(
        vector_store=PineconeVectorStore(
            pinecone_index=MockPineconeIndex(), tokenizer=mock_tokenizer
        )
    )

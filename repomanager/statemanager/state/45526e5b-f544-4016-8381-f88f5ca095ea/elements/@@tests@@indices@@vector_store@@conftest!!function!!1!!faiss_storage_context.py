def faiss_storage_context(faiss_vector_store: FaissVectorStore) -> StorageContext:
    return StorageContext.from_defaults(vector_store=faiss_vector_store)

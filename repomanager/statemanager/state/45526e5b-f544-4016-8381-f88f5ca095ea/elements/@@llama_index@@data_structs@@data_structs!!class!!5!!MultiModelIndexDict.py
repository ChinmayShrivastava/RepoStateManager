class MultiModelIndexDict(IndexDict):
    """A simple dictionary of documents, but loads a MultiModelVectorStore."""

    @classmethod
    def get_type(cls) -> IndexStructType:
        """Get type."""
        return IndexStructType.MULTIMODAL_VECTOR_STORE

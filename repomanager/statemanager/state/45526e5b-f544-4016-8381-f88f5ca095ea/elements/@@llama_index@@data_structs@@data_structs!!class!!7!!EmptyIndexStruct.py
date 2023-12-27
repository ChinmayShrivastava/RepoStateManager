class EmptyIndexStruct(IndexStruct):
    """Empty index."""

    @classmethod
    def get_type(cls) -> IndexStructType:
        """Get type."""
        return IndexStructType.EMPTY

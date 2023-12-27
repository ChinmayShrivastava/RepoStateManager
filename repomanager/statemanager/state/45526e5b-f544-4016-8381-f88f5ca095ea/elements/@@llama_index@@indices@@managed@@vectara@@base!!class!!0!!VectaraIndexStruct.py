class VectaraIndexStruct(IndexDict):
    """Vectara Index Struct."""

    @classmethod
    def get_type(cls) -> IndexStructType:
        """Get index struct type."""
        return IndexStructType.VECTARA

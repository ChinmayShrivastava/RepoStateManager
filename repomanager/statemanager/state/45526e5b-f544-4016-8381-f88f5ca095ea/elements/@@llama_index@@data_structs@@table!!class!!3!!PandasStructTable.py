class PandasStructTable(BaseStructTable):
    """Pandas struct outputs."""

    @classmethod
    def get_type(cls) -> IndexStructType:
        """Get type."""
        return IndexStructType.PANDAS

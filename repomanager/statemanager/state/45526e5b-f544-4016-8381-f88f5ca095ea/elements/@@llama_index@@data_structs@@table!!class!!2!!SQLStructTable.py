class SQLStructTable(BaseStructTable):
    """SQL struct outputs."""

    context_dict: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def get_type(cls) -> IndexStructType:
        """Get type."""
        # TODO: consolidate with IndexStructType
        return IndexStructType.SQL

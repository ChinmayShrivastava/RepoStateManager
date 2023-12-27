class MetadataFilter(BaseModel):
    """Comprehensive metadata filter for vector stores to support more operators.

    Value uses Strict* types, as int, float and str are compatible types and were all
    converted to string before.

    See: https://docs.pydantic.dev/latest/usage/types/#strict-types
    """

    key: str
    value: Union[StrictInt, StrictFloat, StrictStr]
    operator: FilterOperator = FilterOperator.EQ

    @classmethod
    def from_dict(
        cls,
        filter_dict: Dict,
    ) -> "MetadataFilter":
        """Create MetadataFilter from dictionary.

        Args:
            filter_dict: Dict with key, value and operator.

        """
        return MetadataFilter.parse_obj(filter_dict)

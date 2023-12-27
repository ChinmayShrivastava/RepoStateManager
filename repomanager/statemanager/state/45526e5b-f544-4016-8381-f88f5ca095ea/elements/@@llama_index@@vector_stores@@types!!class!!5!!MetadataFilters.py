class MetadataFilters(BaseModel):
    """Metadata filters for vector stores.

    Currently only supports exact match filters.
    TODO: support more advanced expressions.
    """

    # Exact match filters and Advanced filters with operators like >, <, >=, <=, !=, etc.
    filters: List[Union[MetadataFilter, ExactMatchFilter]]
    # and/or such conditions for combining different filters
    condition: Optional[FilterCondition] = FilterCondition.AND

    @classmethod
    @deprecated(
        "`from_dict()` is deprecated. "
        "Please use `MetadataFilters(filters=.., condition='and')` directly instead."
    )
    def from_dict(cls, filter_dict: Dict) -> "MetadataFilters":
        """Create MetadataFilters from json."""
        filters = []
        for k, v in filter_dict.items():
            filter = MetadataFilter(key=k, value=v, operator=FilterOperator.EQ)
            filters.append(filter)
        return cls(filters=filters)

    @classmethod
    def from_dicts(
        cls,
        filter_dicts: List[Dict],
        condition: Optional[FilterCondition] = FilterCondition.AND,
    ) -> "MetadataFilters":
        """Create MetadataFilters from dicts.

        This takes in a list of individual MetadataFilter objects, along
        with the condition.

        Args:
            filter_dicts: List of dicts, each dict is a MetadataFilter.
            condition: FilterCondition to combine different filters.

        """
        return cls(
            filters=[
                MetadataFilter.from_dict(filter_dict) for filter_dict in filter_dicts
            ],
            condition=condition,
        )

    def legacy_filters(self) -> List[ExactMatchFilter]:
        """Convert MetadataFilters to legacy ExactMatchFilters."""
        filters = []
        for filter in self.filters:
            if filter.operator != FilterOperator.EQ:
                raise ValueError(
                    "Vector Store only supports exact match filters. "
                    "Please use ExactMatchFilter or FilterOperator.EQ instead."
                )
            filters.append(ExactMatchFilter(key=filter.key, value=filter.value))
        return filters

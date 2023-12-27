class FilterField:
    name: str
    data_type: str = "string"

    def __init__(self, name: str, data_type: str = "string"):
        self.name = name
        self.data_type = "string" if data_type is None else data_type

    def match_value(self, value: Any) -> bool:
        if self.data_type == "uint64":
            return isinstance(value, int)
        else:
            return isinstance(value, str)

    def to_vdb_filter(self) -> Any:
        from tcvectordb.model.enum import FieldType, IndexType
        from tcvectordb.model.index import FilterIndex

        return FilterIndex(
            name=self.name,
            field_type=FieldType(self.data_type),
            index_type=IndexType.FILTER,
        )

class StructDatapoint(DataClassJsonMixin):
    """Struct outputs."""

    # map from field name to StructValue
    fields: Dict[str, Any]

class RefDocInfo(DataClassJsonMixin):
    """Dataclass to represent ingested documents."""

    node_ids: List = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

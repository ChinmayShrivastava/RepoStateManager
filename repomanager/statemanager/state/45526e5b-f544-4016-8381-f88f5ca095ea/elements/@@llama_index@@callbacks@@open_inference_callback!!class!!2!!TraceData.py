class TraceData:
    """Trace data."""

    query_data: QueryData = field(default_factory=QueryData)
    node_datas: List[NodeData] = field(default_factory=list)

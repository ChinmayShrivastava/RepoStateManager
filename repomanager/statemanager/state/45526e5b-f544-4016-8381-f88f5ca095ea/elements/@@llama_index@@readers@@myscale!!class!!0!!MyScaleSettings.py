class MyScaleSettings:
    """MyScale Client Configuration.

    Attribute:
        table (str) : Table name to operate on.
        database (str) : Database name to find the table.
        index_type (str): index type string
        metric (str) : metric type to compute distance
        batch_size (int): the size of documents to insert
        index_params (dict, optional): index build parameter
        search_params (dict, optional): index search parameters for MyScale query
    """

    def __init__(
        self,
        table: str,
        database: str,
        index_type: str,
        metric: str,
        batch_size: int,
        index_params: Optional[dict] = None,
        search_params: Optional[dict] = None,
        **kwargs: Any,
    ) -> None:
        self.table = table
        self.database = database
        self.index_type = index_type
        self.metric = metric
        self.batch_size = batch_size
        self.index_params = index_params
        self.search_params = search_params

    def build_query_statement(
        self,
        query_embed: List[float],
        where_str: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> str:
        query_embed_str = format_list_to_string(query_embed)
        where_str = f"PREWHERE {where_str}" if where_str else ""
        order = "DESC" if self.metric.lower() == "ip" else "ASC"

        search_params_str = (
            (
                "("
                + ",".join([f"'{k}={v}'" for k, v in self.search_params.items()])
                + ")"
            )
            if self.search_params
            else ""
        )

        return f"""
            SELECT id, doc_id, text, node_info, metadata,
            distance{search_params_str}(vector, {query_embed_str}) AS dist
            FROM {self.database}.{self.table} {where_str}
            ORDER BY dist {order}
            LIMIT {limit}
            """

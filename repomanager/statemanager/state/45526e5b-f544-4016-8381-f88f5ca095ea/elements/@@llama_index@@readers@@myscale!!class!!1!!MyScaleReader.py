class MyScaleReader(BaseReader):
    """MyScale reader.

    Args:
        myscale_host (str) : An URL to connect to MyScale backend.
        username (str) : Usernamed to login.
        password (str) : Password to login.
        myscale_port (int) : URL port to connect with HTTP. Defaults to 8443.
        database (str) : Database name to find the table. Defaults to 'default'.
        table (str) : Table name to operate on. Defaults to 'vector_table'.
        index_type (str): index type string. Default to "IVFLAT"
        metric (str) : Metric to compute distance, supported are ('l2', 'cosine', 'ip').
            Defaults to 'cosine'
        batch_size (int, optional): the size of documents to insert. Defaults to 32.
        index_params (dict, optional): The index parameters for MyScale.
            Defaults to None.
        search_params (dict, optional): The search parameters for a MyScale query.
            Defaults to None.

    """

    def __init__(
        self,
        myscale_host: str,
        username: str,
        password: str,
        myscale_port: Optional[int] = 8443,
        database: str = "default",
        table: str = "llama_index",
        index_type: str = "IVFLAT",
        metric: str = "cosine",
        batch_size: int = 32,
        index_params: Optional[dict] = None,
        search_params: Optional[dict] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize params."""
        import_err_msg = """
            `clickhouse_connect` package not found,
            please run `pip install clickhouse-connect`
        """
        try:
            import clickhouse_connect
        except ImportError:
            raise ImportError(import_err_msg)

        self.client = clickhouse_connect.get_client(
            host=myscale_host,
            port=myscale_port,
            username=username,
            password=password,
        )

        self.config = MyScaleSettings(
            table=table,
            database=database,
            index_type=index_type,
            metric=metric,
            batch_size=batch_size,
            index_params=index_params,
            search_params=search_params,
            **kwargs,
        )

    def load_data(
        self,
        query_vector: List[float],
        where_str: Optional[str] = None,
        limit: int = 10,
    ) -> List[Document]:
        """Load data from MyScale.

        Args:
            query_vector (List[float]): Query vector.
            where_str (Optional[str], optional): where condition string.
                Defaults to None.
            limit (int): Number of results to return.

        Returns:
            List[Document]: A list of documents.
        """
        query_statement = self.config.build_query_statement(
            query_embed=query_vector,
            where_str=where_str,
            limit=limit,
        )

        return [
            Document(id_=r["doc_id"], text=r["text"], metadata=r["metadata"])
            for r in self.client.query(query_statement).named_results()
        ]

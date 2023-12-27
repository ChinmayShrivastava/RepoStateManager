class PGVectorSQLParser(BaseSQLParser):
    """PGVector SQL Parser."""

    def __init__(
        self,
        embed_model: BaseEmbedding,
    ) -> None:
        """Initialize params."""
        self._embed_model = embed_model

    def parse_response_to_sql(self, response: str, query_bundle: QueryBundle) -> str:
        """Parse response to SQL."""
        sql_query_start = response.find("SQLQuery:")
        if sql_query_start != -1:
            response = response[sql_query_start:]
            # TODO: move to removeprefix after Python 3.9+
            if response.startswith("SQLQuery:"):
                response = response[len("SQLQuery:") :]
        sql_result_start = response.find("SQLResult:")
        if sql_result_start != -1:
            response = response[:sql_result_start]

        # this gets you the sql string with [query_vector] placeholders
        raw_sql_str = response.strip().strip("```").strip()
        query_embedding = self._embed_model.get_query_embedding(query_bundle.query_str)
        query_embedding_str = str(query_embedding)
        return raw_sql_str.replace("[query_vector]", query_embedding_str)

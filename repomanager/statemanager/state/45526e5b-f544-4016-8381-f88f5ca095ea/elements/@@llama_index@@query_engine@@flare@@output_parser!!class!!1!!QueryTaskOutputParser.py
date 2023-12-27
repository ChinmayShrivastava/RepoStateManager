class QueryTaskOutputParser(BaseOutputParser):
    """QueryTask output parser.

    By default, parses output that contains "[Search(query)]" tags.

    """

    def parse(self, output: str) -> Any:
        """Parse output."""
        query_tasks = []
        for idx, char in enumerate(output):
            if char == "[":
                start_idx = idx
            elif char == "]":
                end_idx = idx
                raw_query_str = output[start_idx + 1 : end_idx]
                query_str = raw_query_str.split("(")[1].split(")")[0]
                query_tasks.append(QueryTask(query_str, start_idx, end_idx))
        return query_tasks

    def format(self, output: str) -> str:
        """Format a query with structured output formatting instructions."""
        raise NotImplementedError

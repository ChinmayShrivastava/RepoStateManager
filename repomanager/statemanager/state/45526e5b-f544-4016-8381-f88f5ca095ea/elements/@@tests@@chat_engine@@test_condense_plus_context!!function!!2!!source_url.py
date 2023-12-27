    def source_url(query: str) -> str:
        query_url = query.replace(" ", "_")
        # limit to first 10 characters
        query_url = query_url[:10]
        return f"http://example.com/{query_url}"

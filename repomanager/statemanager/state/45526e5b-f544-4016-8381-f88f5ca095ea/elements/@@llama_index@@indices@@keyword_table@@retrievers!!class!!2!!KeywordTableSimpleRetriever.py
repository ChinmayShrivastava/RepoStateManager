class KeywordTableSimpleRetriever(BaseKeywordTableRetriever):
    """Keyword Table Index Simple Retriever.

    Extracts keywords using simple regex-based keyword extractor.
    Set when `retriever_mode="simple"`.

    See BaseGPTKeywordTableQuery for arguments.

    """

    def _get_keywords(self, query_str: str) -> List[str]:
        """Extract keywords."""
        return list(
            simple_extract_keywords(query_str, max_keywords=self.max_keywords_per_query)
        )

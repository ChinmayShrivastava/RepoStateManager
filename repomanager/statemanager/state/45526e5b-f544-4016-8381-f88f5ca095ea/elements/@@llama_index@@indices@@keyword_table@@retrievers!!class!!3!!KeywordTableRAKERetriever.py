class KeywordTableRAKERetriever(BaseKeywordTableRetriever):
    """Keyword Table Index RAKE Retriever.

    Extracts keywords using RAKE keyword extractor.
    Set when `retriever_mode="rake"`.

    See BaseGPTKeywordTableQuery for arguments.

    """

    def _get_keywords(self, query_str: str) -> List[str]:
        """Extract keywords."""
        return list(
            rake_extract_keywords(query_str, max_keywords=self.max_keywords_per_query)
        )

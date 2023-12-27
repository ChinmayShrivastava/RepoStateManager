class KeywordTableGPTRetriever(BaseKeywordTableRetriever):
    """Keyword Table Index GPT Retriever.

    Extracts keywords using GPT. Set when using `retriever_mode="default"`.

    See BaseGPTKeywordTableQuery for arguments.

    """

    def _get_keywords(self, query_str: str) -> List[str]:
        """Extract keywords."""
        response = self._service_context.llm.predict(
            self.query_keyword_extract_template,
            max_keywords=self.max_keywords_per_query,
            question=query_str,
        )
        keywords = extract_keywords_given_response(response, start_token="KEYWORDS:")
        return list(keywords)

class KeywordTableIndex(BaseKeywordTableIndex):
    """Keyword Table Index.

    This index uses a GPT model to extract keywords from the text.

    """

    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract keywords from text."""
        response = self._service_context.llm.predict(
            self.keyword_extract_template,
            text=text,
        )
        return extract_keywords_given_response(response, start_token="KEYWORDS:")

    async def _async_extract_keywords(self, text: str) -> Set[str]:
        """Extract keywords from text."""
        response = await self._service_context.llm.apredict(
            self.keyword_extract_template,
            text=text,
        )
        return extract_keywords_given_response(response, start_token="KEYWORDS:")

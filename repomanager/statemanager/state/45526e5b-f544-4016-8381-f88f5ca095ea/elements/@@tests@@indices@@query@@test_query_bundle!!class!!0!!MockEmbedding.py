class MockEmbedding(BaseEmbedding):
    @classmethod
    def class_name(cls) -> str:
        return "MockEmbedding"

    async def _aget_query_embedding(self, query: str) -> List[float]:
        text_embed_map: Dict[str, List[float]] = {
            "It is what it is.": [1.0, 0.0, 0.0, 0.0, 0.0],
            "The meaning of life": [0.0, 1.0, 0.0, 0.0, 0.0],
        }

        return text_embed_map[query]

    async def _aget_text_embedding(self, text: str) -> List[float]:
        text_embed_map: Dict[str, List[float]] = {
            "Correct.": [0.5, 0.5, 0.0, 0.0, 0.0],
            "Hello world.": [1.0, 0.0, 0.0, 0.0, 0.0],
            "This is a test.": [0.0, 1.0, 0.0, 0.0, 0.0],
            "This is another test.": [0.0, 0.0, 1.0, 0.0, 0.0],
            "This is a test v2.": [0.0, 0.0, 0.0, 1.0, 0.0],
        }

        return text_embed_map[text]

    def _get_text_embedding(self, text: str) -> List[float]:
        """Get node text embedding."""
        text_embed_map: Dict[str, List[float]] = {
            "Correct.": [0.5, 0.5, 0.0, 0.0, 0.0],
            "Hello world.": [1.0, 0.0, 0.0, 0.0, 0.0],
            "This is a test.": [0.0, 1.0, 0.0, 0.0, 0.0],
            "This is another test.": [0.0, 0.0, 1.0, 0.0, 0.0],
            "This is a test v2.": [0.0, 0.0, 0.0, 1.0, 0.0],
        }

        return text_embed_map[text]

    def _get_query_embedding(self, query: str) -> List[float]:
        """Get query embedding."""
        text_embed_map: Dict[str, List[float]] = {
            "It is what it is.": [1.0, 0.0, 0.0, 0.0, 0.0],
            "The meaning of life": [0.0, 1.0, 0.0, 0.0, 0.0],
        }

        return text_embed_map[query]

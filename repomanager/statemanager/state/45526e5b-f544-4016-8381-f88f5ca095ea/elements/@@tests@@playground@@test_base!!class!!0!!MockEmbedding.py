class MockEmbedding(BaseEmbedding):
    @classmethod
    def class_name(cls) -> str:
        return "MockEmbedding"

    async def _aget_query_embedding(self, query: str) -> List[float]:
        del query
        return [0, 0, 1, 0, 0]

    async def _aget_text_embedding(self, text: str) -> List[float]:
        # assume dimensions are 5
        if text == "They're taking the Hobbits to Isengard!":
            return [1, 0, 0, 0, 0]
        elif text == "I can't carry it for you.":
            return [0, 1, 0, 0, 0]
        elif text == "But I can carry you!":
            return [0, 0, 1, 0, 0]
        else:
            raise ValueError("Invalid text for `mock_get_text_embedding`.")

    def _get_text_embedding(self, text: str) -> List[float]:
        """Mock get text embedding."""
        # assume dimensions are 5
        if text == "They're taking the Hobbits to Isengard!":
            return [1, 0, 0, 0, 0]
        elif text == "I can't carry it for you.":
            return [0, 1, 0, 0, 0]
        elif text == "But I can carry you!":
            return [0, 0, 1, 0, 0]
        else:
            raise ValueError("Invalid text for `mock_get_text_embedding`.")

    def _get_query_embedding(self, query: str) -> List[float]:
        """Mock get query embedding."""
        del query
        return [0, 0, 1, 0, 0]

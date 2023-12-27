class MockEmbedding(BaseEmbedding):
    @classmethod
    def class_name(cls) -> str:
        return "MockEmbedding"

    async def _aget_query_embedding(self, query: str) -> List[float]:
        del query
        return [0, 0, 1, 0, 0]

    async def _aget_text_embedding(self, text: str) -> List[float]:
        # assume dimensions are 4
        if text == "('foo', 'is', 'bar')":
            return [1, 0, 0, 0]
        elif text == "('hello', 'is not', 'world')":
            return [0, 1, 0, 0]
        elif text == "('Jane', 'is mother of', 'Bob')":
            return [0, 0, 1, 0]
        elif text == "foo":
            return [0, 0, 0, 1]
        else:
            raise ValueError("Invalid text for `mock_get_text_embedding`.")

    def _get_text_embedding(self, text: str) -> List[float]:
        """Mock get text embedding."""
        # assume dimensions are 4
        if text == "('foo', 'is', 'bar')":
            return [1, 0, 0, 0]
        elif text == "('hello', 'is not', 'world')":
            return [0, 1, 0, 0]
        elif text == "('Jane', 'is mother of', 'Bob')":
            return [0, 0, 1, 0]
        elif text == "foo":
            return [0, 0, 0, 1]
        else:
            raise ValueError("Invalid text for `mock_get_text_embedding`.")

    def _get_query_embedding(self, query: str) -> List[float]:
        """Mock get query embedding."""
        del query
        return [0, 0, 1, 0, 0]

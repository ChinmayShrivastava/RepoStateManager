class MockEmbedding(BaseEmbedding):
    @classmethod
    def class_name(cls) -> str:
        return "MockEmbedding"

    async def _aget_query_embedding(self, query: str) -> List[float]:
        if query == "Foo?":
            return [0, 0, 1, 0, 0]
        elif query == "Orange?":
            return [0, 1, 0, 0, 0]
        elif query == "Cat?":
            return [0, 0, 0, 1, 0]
        else:
            raise ValueError("Invalid query for `_get_query_embedding`.")

    async def _aget_text_embedding(self, text: str) -> List[float]:
        # assume dimensions are 5
        if text == "Hello world.":
            return [1, 0, 0, 0, 0]
        elif text == "This is a test.":
            return [0, 1, 0, 0, 0]
        elif text == "This is another test.":
            return [0, 0, 1, 0, 0]
        elif text == "This is a test v2.":
            return [0, 0, 0, 1, 0]
        elif text == "foo bar":
            return [0, 0, 1, 0, 0]
        elif text == "apple orange":
            return [0, 1, 0, 0, 0]
        elif text == "toronto london":
            return [1, 0, 0, 0, 0]
        elif text == "cat dog":
            return [0, 0, 0, 1, 0]
        else:
            raise ValueError("Invalid text for `mock_get_text_embedding`.")

    def _get_query_embedding(self, query: str) -> List[float]:
        """Mock get query embedding."""
        if query == "Foo?":
            return [0, 0, 1, 0, 0]
        elif query == "Orange?":
            return [0, 1, 0, 0, 0]
        elif query == "Cat?":
            return [0, 0, 0, 1, 0]
        else:
            raise ValueError("Invalid query for `_get_query_embedding`.")

    def _get_text_embedding(self, text: str) -> List[float]:
        """Mock get text embedding."""
        # assume dimensions are 5
        if text == "Hello world.":
            return [1, 0, 0, 0, 0]
        elif text == "This is a test.":
            return [0, 1, 0, 0, 0]
        elif text == "This is another test.":
            return [0, 0, 1, 0, 0]
        elif text == "This is a test v2.":
            return [0, 0, 0, 1, 0]
        elif text == "foo bar":
            return [0, 0, 1, 0, 0]
        elif text == "apple orange":
            return [0, 1, 0, 0, 0]
        elif text == "toronto london":
            return [1, 0, 0, 0, 0]
        elif text == "cat dog":
            return [0, 0, 0, 1, 0]
        else:
            raise ValueError("Invalid text for `mock_get_text_embedding`.")

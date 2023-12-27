class MockMongoClient:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._db = MockMongoDB()

    def __getitem__(self, db: str) -> MockMongoDB:
        del db
        return self._db

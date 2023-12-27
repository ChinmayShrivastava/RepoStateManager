class MockMongoDB:
    def __init__(self) -> None:
        self._collections: Dict[str, MockMongoCollection] = defaultdict(
            MockMongoCollection
        )

    def __getitem__(self, collection: str) -> MockMongoCollection:
        return self._collections[collection]

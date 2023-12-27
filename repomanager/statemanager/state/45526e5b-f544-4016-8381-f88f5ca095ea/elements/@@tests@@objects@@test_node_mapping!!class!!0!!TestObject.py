class TestObject(BaseModel):
    """Test object for node mapping."""

    __test__ = False

    name: str

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return f"TestObject(name='{self.name}')"

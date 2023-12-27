class TestNestedModel(BaseModel):
    __test__ = False
    attr2: List[TestSimpleModel]

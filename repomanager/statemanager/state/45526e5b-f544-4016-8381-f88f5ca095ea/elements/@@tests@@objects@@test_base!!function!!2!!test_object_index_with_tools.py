def test_object_index_with_tools(mock_service_context: ServiceContext) -> None:
    """Test object index with tools."""
    tool1 = FunctionTool.from_defaults(fn=lambda x: x, name="test_tool")
    tool2 = FunctionTool.from_defaults(fn=lambda x, y: x + y, name="test_tool2")

    object_mapping = SimpleToolNodeMapping.from_objects([tool1, tool2])

    obj_retriever = ObjectIndex.from_objects(
        [tool1, tool2], object_mapping, index_cls=SummaryIndex
    )
    assert obj_retriever.as_retriever().retrieve("test") == [tool1, tool2]

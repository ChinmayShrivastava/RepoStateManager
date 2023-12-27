def test_tool_object_node_mapping() -> None:
    """Test tool object node mapping."""
    tool1 = FunctionTool.from_defaults(
        fn=lambda x: x,
        name="test_tool",
        description="test",
    )
    tool2 = FunctionTool.from_defaults(
        fn=lambda x, y: x + y, name="test_tool2", description="test"
    )

    node_mapping = SimpleToolNodeMapping.from_objects([tool1, tool2])
    # don't need to check for tool fn schema
    assert (
        "Tool name: test_tool\n" "Tool description: test\n"
    ) in node_mapping.to_node(tool1).get_text()
    assert node_mapping.from_node(node_mapping.to_node(tool1)) == tool1
    assert (
        "Tool name: test_tool2\n" "Tool description: test\n"
    ) in node_mapping.to_node(tool2).get_text()
    recon_tool2 = node_mapping.from_node(node_mapping.to_node(tool2))
    assert recon_tool2(1, 2).raw_output == 3

    tool3 = FunctionTool.from_defaults(
        fn=lambda x, y: x * y, name="test_tool3", description="test3"
    )
    node_mapping.add_object(tool3)
    assert (
        "Tool name: test_tool3\n" "Tool description: test3\n"
    ) in node_mapping.to_node(tool3).get_text()
    assert node_mapping.from_node(node_mapping.to_node(tool3)) == tool3

def test_ondemand_loader_tool(
    tool: OnDemandLoaderTool,
) -> None:
    """Test ondemand loader."""
    response = tool(["Hello world."], query_str="What is?")
    assert str(response) == "What is?:Hello world."

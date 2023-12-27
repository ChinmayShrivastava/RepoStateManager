def test_ondemand_loader_tool_langchain(
    tool: OnDemandLoaderTool,
) -> None:
    # convert tool to structured langchain tool
    lc_tool = tool.to_langchain_structured_tool()
    assert lc_tool.args_schema == TestSchemaSpec
    response = lc_tool.run({"texts": ["Hello world."], "query_str": "What is?"})
    assert str(response) == "What is?:Hello world."

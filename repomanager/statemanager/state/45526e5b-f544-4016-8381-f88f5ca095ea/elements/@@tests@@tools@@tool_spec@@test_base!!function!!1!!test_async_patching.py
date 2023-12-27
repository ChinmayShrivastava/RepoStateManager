def test_async_patching() -> None:
    # test sync patching of async function
    tool_spec = TestToolSpec()
    tool_spec.spec_functions = ["afoo"]
    tools = tool_spec.to_tool_list()
    assert len(tools) == 1
    assert tools[0].fn("hello", 1) == "foo hello 1"

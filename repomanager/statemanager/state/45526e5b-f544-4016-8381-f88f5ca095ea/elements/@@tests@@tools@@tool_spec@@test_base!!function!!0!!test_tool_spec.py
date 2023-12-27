def test_tool_spec() -> None:
    """Test tool spec."""
    tool_spec = TestToolSpec()
    # first is foo, second is bar
    tools = tool_spec.to_tool_list()
    assert len(tools) == 3
    assert tools[0].metadata.name == "foo"
    assert tools[0].metadata.description == "foo(arg1: str, arg2: int) -> str\nFoo."
    assert tools[0].fn("hello", 1) == "foo hello 1"
    assert tools[1].metadata.name == "bar"
    assert tools[1].metadata.description == "bar(arg1: bool) -> str\nBar."
    assert str(tools[1](True)) == "bar True"
    assert tools[2].metadata.name == "abc"
    assert tools[2].metadata.description == "abc(arg1: str) -> str\n"
    assert tools[2].metadata.fn_schema == AbcSchema

    # test metadata mapping
    tools = tool_spec.to_tool_list(
        func_to_metadata_mapping={
            "foo": ToolMetadata(
                "foo_description", name="foo_name", fn_schema=FooSchema
            ),
        }
    )
    assert len(tools) == 3
    assert tools[0].metadata.name == "foo_name"
    assert tools[0].metadata.description == "foo_description"
    assert tools[0].metadata.fn_schema is not None
    fn_schema = tools[0].metadata.fn_schema.schema()
    print(fn_schema)
    assert fn_schema["properties"]["arg1"]["type"] == "string"
    assert fn_schema["properties"]["arg2"]["type"] == "integer"
    assert tools[1].metadata.name == "bar"
    assert tools[1].metadata.description == "bar(arg1: bool) -> str\nBar."
    assert tools[1].metadata.fn_schema is not None
    fn_schema = tools[1].metadata.fn_schema.schema()
    assert fn_schema["properties"]["arg1"]["type"] == "boolean"

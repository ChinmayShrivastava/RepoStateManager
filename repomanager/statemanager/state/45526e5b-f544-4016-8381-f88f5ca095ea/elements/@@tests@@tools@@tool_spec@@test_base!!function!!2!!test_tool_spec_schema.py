def test_tool_spec_schema() -> None:
    """Test tool spec schemas match."""
    tool_spec = TestToolSpec()
    # first is foo, second is bar
    schema1 = tool_spec.get_fn_schema_from_fn_name("foo")
    assert schema1 == FooSchema
    schema2 = tool_spec.get_fn_schema_from_fn_name("bar")
    assert schema2 == BarSchema

def test_call_tool_with_error_handling() -> None:
    """Test call tool with error handling."""

    def _add(a: int, b: int) -> int:
        return a + b

    tool = FunctionTool.from_defaults(fn=_add)

    output = call_tool_with_error_handling(
        tool, {"a": 1, "b": 1}, error_message="Error!"
    )
    assert output.content == "2"

    # try error
    output = call_tool_with_error_handling(
        tool, {"a": "1", "b": 1}, error_message="Error!"
    )
    assert output.content == "Error!"

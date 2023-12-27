def test_extract_tool_number() -> None:
    mock_input_text = """\
Thought: I need to use a tool to help me answer the question.
Action: add2
Action Input: {"a": 1, "b": 1}
"""
    thought, action, action_input = extract_tool_use(mock_input_text)
    assert thought == "I need to use a tool to help me answer the question."
    assert action == "add2"
    assert action_input == '{"a": 1, "b": 1}'

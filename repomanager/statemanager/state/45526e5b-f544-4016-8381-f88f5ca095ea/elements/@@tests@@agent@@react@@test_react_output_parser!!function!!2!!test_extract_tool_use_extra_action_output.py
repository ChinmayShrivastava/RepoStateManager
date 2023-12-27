def test_extract_tool_use_extra_action_output() -> None:
    mock_input_text = """\
Thought: I need to use a tool to help me answer the question.
Action: add (add two numbers)
Action Input: {"a": 1, "b": 1}
"""
    thought, action, action_input = extract_tool_use(mock_input_text)
    assert thought == "I need to use a tool to help me answer the question."
    assert action == "add"
    assert action_input == '{"a": 1, "b": 1}'

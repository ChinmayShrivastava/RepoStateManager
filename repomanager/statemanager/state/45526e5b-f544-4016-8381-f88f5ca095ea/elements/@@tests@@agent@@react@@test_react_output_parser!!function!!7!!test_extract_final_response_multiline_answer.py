def test_extract_final_response_multiline_answer() -> None:
    mock_input_text = """\
Thought: I have enough information to answer the question without using any more tools.
Answer: Here is the answer:

This is the second line.
"""

    expected_thought = (
        "I have enough information to answer the question "
        "without using any more tools."
    )
    thought, answer = extract_final_response(mock_input_text)
    assert thought == expected_thought
    assert (
        answer
        == """Here is the answer:

This is the second line."""
    )

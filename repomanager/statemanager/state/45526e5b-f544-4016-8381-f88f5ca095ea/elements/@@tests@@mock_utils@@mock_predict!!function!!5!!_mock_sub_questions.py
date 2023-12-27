def _mock_sub_questions() -> str:
    """Mock sub questions."""
    json_str = json.dumps(
        [
            {
                "sub_question": "mock question for source_1",
                "tool_name": "source_1",
            }
        ],
        indent=4,
    )
    return f"```json\n{json_str}\n```"

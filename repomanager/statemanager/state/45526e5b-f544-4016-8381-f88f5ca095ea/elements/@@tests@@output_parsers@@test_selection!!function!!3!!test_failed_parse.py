def test_failed_parse(output_parser: SelectionOutputParser) -> None:
    no_json_in_response = (
        " Based on the given choices, the most relevant choice for the question"
        " 'What are the <redacted>?' is:\n\n(1) <redacted>.\n\nThe reason for"
        " this choice is that <redacted>. Therefore, choosing option (1) would"
        " provide the most relevant information for finding the <redacted>."
    )
    with pytest.raises(ValueError, match="Failed to convert*") as exc_info:
        output_parser.parse(output=no_json_in_response)

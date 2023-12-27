def test_parse(
    output_parser: SelectionOutputParser, output: str, num_match: int
) -> None:
    parsed = output_parser.parse(output=output)
    assert isinstance(parsed, StructuredOutput)
    assert isinstance(parsed.parsed_output, list)
    assert len(parsed.parsed_output) == num_match
    assert parsed.parsed_output[0].choice == 1
    assert parsed.parsed_output[0].reason == "just because"

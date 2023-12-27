def _mock_output_parser(output: str) -> Optional[Dict[str, Any]]:
    """Mock output parser.

    Split via commas instead of newlines, in order to fit
    the format of the mock test document (newlines create
    separate text chunks in the testing code).

    """
    tups = output.split(",")

    fields = {}
    for tup in tups:
        if ":" in tup:
            tokens = tup.split(":")
            field = re.sub(r"\W+", "", tokens[0])
            value = re.sub(r"\W+", "", tokens[1])
            fields[field] = value
    return fields

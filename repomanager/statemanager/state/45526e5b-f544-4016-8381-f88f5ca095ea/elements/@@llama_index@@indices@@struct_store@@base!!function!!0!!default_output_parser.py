def default_output_parser(output: str) -> Optional[Dict[str, Any]]:
    """Parse output of schema extraction.

    Attempt to parse the following format from the default prompt:
    field1: <value>, field2: <value>, ...

    """
    tups = output.split("\n")

    fields = {}
    for tup in tups:
        if ":" in tup:
            tokens = tup.split(":")
            field = re.sub(r"\W+", "", tokens[0])
            value = re.sub(r"\W+", "", tokens[1])
            fields[field] = value
    return fields

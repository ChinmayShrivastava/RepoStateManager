def _mock_text_to_sql(prompt_args: Dict) -> str:
    """Mock text to sql."""
    # assume it's a select query
    tokens = prompt_args["query_str"].split(":")
    table_name = tokens[0]
    subtokens = tokens[1].split(",")
    return "SELECT " + ", ".join(subtokens) + f" FROM {table_name}"

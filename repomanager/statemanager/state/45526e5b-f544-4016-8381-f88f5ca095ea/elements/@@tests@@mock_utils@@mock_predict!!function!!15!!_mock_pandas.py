def _mock_pandas(prompt_args: Dict) -> str:
    """Mock pandas prompt."""
    query_str = prompt_args["query_str"]
    return f'df["{query_str}"]'

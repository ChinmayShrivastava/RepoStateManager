def _mock_decompose_query(prompt_args: Dict) -> str:
    """Mock decompose query."""
    return prompt_args["query_str"] + ":" + prompt_args["context_str"]

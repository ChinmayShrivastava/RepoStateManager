def _mock_query_select_multiple(num_chunks: int) -> str:
    """Mock query select."""
    nums_str = ", ".join([str(i) for i in range(num_chunks)])
    return f"ANSWER: {nums_str}"

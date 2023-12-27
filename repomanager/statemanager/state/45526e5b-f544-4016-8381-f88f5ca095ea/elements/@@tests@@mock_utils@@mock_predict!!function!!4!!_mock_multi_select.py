def _mock_multi_select(prompt_args: Dict) -> str:
    """Mock single select."""
    answers = [
        {
            "choice": 1,
            "reason": "test",
        },
        {
            "choice": 2,
            "reason": "test",
        },
        {
            "choice": 3,
            "reason": "test",
        },
    ]
    max_outputs = prompt_args["max_outputs"]
    answers = answers[:max_outputs]

    return json.dumps(answers)

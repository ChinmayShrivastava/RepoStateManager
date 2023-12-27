def _mock_single_select() -> str:
    """Mock single select."""
    return json.dumps(
        [
            {
                "choice": 1,
                "reason": "test",
            }
        ]
    )

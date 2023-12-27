def _mock_obj_function(param_dict: Dict) -> RunResult:
    """Mock obj function."""
    return RunResult(
        score=int(param_dict["a"]) + int(param_dict["b"]) + int(param_dict["c"]),
        params=param_dict,
    )

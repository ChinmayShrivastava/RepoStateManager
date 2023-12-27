def test_param_tuner() -> None:
    """Test param tuner."""
    param_dict = {"a": [1, 2, 3], "b": [4, 5, 6]}
    fixed_param_dict = {"c": 5}
    # try sync version
    tuner = ParamTuner(
        param_dict=param_dict,
        fixed_param_dict=fixed_param_dict,
        param_fn=_mock_obj_function,
    )
    result = tuner.tune()
    assert result.best_run_result.score == 14
    assert result.best_run_result.params["a"] == 3
    assert result.best_run_result.params["b"] == 6

    # try async version
    atuner = AsyncParamTuner(
        param_dict=param_dict,
        fixed_param_dict=fixed_param_dict,
        aparam_fn=_amock_obj_function,
    )
    # should run synchronous fn
    result = atuner.tune()
    assert result.best_run_result.score == 4
    assert result.best_run_result.params["a"] == 3
    assert result.best_run_result.params["b"] == 4

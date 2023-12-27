def test_init() -> None:
    dummy = RunGptLLM(model="mock model", endpoint="0.0.0.0:51002")
    assert dummy.model == "mock model"
    assert dummy.endpoint == "0.0.0.0:51002"
    assert isinstance(dummy, RunGptLLM)

def test_init() -> None:
    dummy = MockXinference(
        model_uid="uid",
        endpoint="endpoint",
    )
    assert dummy.model_uid == "uid"
    assert dummy.endpoint == "endpoint"
    assert isinstance(dummy.temperature, float)
    assert dummy.temperature == 1.0
    assert isinstance(dummy.max_tokens, int)
    assert dummy.max_tokens == dummy.context_window // 4

    dummy_custom = MockXinference(
        model_uid="uid_custom",
        endpoint="endpoint_custom",
        temperature=(dummy.temperature + 0.1) / 2,
        max_tokens=dummy.max_tokens + 2,
    )
    assert dummy_custom.model_uid == "uid_custom"
    assert dummy_custom.endpoint == "endpoint_custom"
    assert isinstance(dummy_custom.temperature, float)
    assert dummy_custom.temperature != dummy.temperature
    assert dummy_custom.temperature == (dummy.temperature + 0.1) / 2
    assert isinstance(dummy_custom.max_tokens, int)
    assert dummy_custom.max_tokens != dummy.max_tokens
    assert dummy_custom.max_tokens == dummy.max_tokens + 2

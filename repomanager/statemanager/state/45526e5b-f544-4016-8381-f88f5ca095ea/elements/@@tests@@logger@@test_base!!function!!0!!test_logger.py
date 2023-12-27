def test_logger() -> None:
    """Test logger."""
    logger = LlamaLogger()
    # test add
    for i in range(4):
        logger.add_log({"foo": "bar", "item": i})
    logs = logger.get_logs()
    assert logs == [
        {"foo": "bar", "item": 0},
        {"foo": "bar", "item": 1},
        {"foo": "bar", "item": 2},
        {"foo": "bar", "item": 3},
    ]

    # test reset
    logger.reset()
    assert logger.get_logs() == []

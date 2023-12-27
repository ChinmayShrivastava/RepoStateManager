def test_ignore_events() -> None:
    """Test ignore event starts and ends."""
    handler = LlamaDebugHandler(
        event_starts_to_ignore=[CBEventType.CHUNKING],
        event_ends_to_ignore=[CBEventType.LLM],
    )
    manager = CallbackManager([handler])

    event_id = manager.on_event_start(CBEventType.CHUNKING, payload=TEST_PAYLOAD)
    manager.on_event_end(CBEventType.CHUNKING, event_id=event_id)

    event_id = manager.on_event_start(CBEventType.LLM, payload=TEST_PAYLOAD)
    manager.on_event_end(CBEventType.LLM, event_id=event_id)

    event_id = manager.on_event_start(CBEventType.EMBEDDING, payload=TEST_PAYLOAD)
    manager.on_event_end(CBEventType.EMBEDDING, event_id=event_id)

    # should have only captured 6 - 2 = 4 events
    assert len(handler.sequential_events) == 4

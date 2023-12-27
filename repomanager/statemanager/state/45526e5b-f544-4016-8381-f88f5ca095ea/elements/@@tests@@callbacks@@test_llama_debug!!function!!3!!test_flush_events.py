def test_flush_events() -> None:
    """Test flush events."""
    handler = LlamaDebugHandler()

    event_id = handler.on_event_start(CBEventType.CHUNKING, payload=TEST_PAYLOAD)
    handler.on_event_end(CBEventType.CHUNKING, event_id=event_id)

    event_id = handler.on_event_start(CBEventType.CHUNKING, payload=TEST_PAYLOAD)
    handler.on_event_end(CBEventType.CHUNKING, event_id=event_id)

    assert len(handler.event_pairs_by_type[CBEventType.CHUNKING]) == 4

    handler.flush_event_logs()

    assert len(handler.event_pairs_by_type) == 0
    assert len(handler.sequential_events) == 0

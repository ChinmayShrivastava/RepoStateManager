def test_get_event_stats() -> None:
    """Test get event stats."""
    handler = LlamaDebugHandler()

    event_id = handler.on_event_start(CBEventType.CHUNKING, payload=TEST_PAYLOAD)
    handler.on_event_end(CBEventType.CHUNKING, event_id=event_id)

    assert len(handler.event_pairs_by_type[CBEventType.CHUNKING]) == 2

    event_stats = handler.get_event_time_info(CBEventType.CHUNKING)

    assert event_stats.total_count == 1
    assert event_stats.total_secs > 0.0

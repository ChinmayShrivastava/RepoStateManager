def test_on_event_end() -> None:
    """Test event end."""
    handler = LlamaDebugHandler()

    handler.on_event_end(CBEventType.EMBEDDING, payload=TEST_PAYLOAD, event_id=TEST_ID)

    assert len(handler.event_pairs_by_type) == 1
    assert len(handler.sequential_events) == 1

    events = handler.event_pairs_by_type.get(CBEventType.EMBEDDING)
    assert isinstance(events, list)
    assert events[0].payload == TEST_PAYLOAD
    assert events[0].id_ == TEST_ID

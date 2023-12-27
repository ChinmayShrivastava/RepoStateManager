def test_on_event_start() -> None:
    """Test event start."""
    handler = LlamaDebugHandler()

    event_id = handler.on_event_start(
        CBEventType.LLM, payload=TEST_PAYLOAD, event_id=TEST_ID
    )

    assert event_id == TEST_ID
    assert len(handler.event_pairs_by_type) == 1
    assert len(handler.sequential_events) == 1

    events = handler.event_pairs_by_type.get(CBEventType.LLM)
    assert isinstance(events, list)
    assert events[0].payload == TEST_PAYLOAD

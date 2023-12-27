def test_on_event_end() -> None:
    """Test event end."""
    handler = TokenCountingHandler()

    handler.on_event_end(CBEventType.LLM, payload=TEST_PAYLOAD, event_id=TEST_ID)

    assert len(handler.llm_token_counts) == 1
    assert len(handler.embedding_token_counts) == 0

    handler.on_event_end(CBEventType.EMBEDDING, payload=TEST_PAYLOAD, event_id=TEST_ID)

    assert len(handler.llm_token_counts) == 1
    assert len(handler.embedding_token_counts) == 1

    assert handler.embedding_token_counts[0].total_token_count == 1
    assert handler.llm_token_counts[0].total_token_count == 2

    # test actual counts
    # LLM should be two (prompt plus response)
    # Embedding should be one (single token chunk)
    assert handler.total_llm_token_count == 2
    assert handler.total_embedding_token_count == 1

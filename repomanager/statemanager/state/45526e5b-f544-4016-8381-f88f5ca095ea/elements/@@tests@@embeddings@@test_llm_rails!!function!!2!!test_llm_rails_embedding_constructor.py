def test_llm_rails_embedding_constructor(model_id: str, api_key: str) -> None:
    """Test LLMRails embedding constructor."""
    LLMRailsEmbedding(model_id=model_id, api_key=api_key)

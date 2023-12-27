def mock_llmpredictor_predict(
    self: Any, prompt: BasePromptTemplate, **prompt_args: Any
) -> str:
    """Patch llm predictor predict."""
    return "Doc: 2, Relevance: 5"

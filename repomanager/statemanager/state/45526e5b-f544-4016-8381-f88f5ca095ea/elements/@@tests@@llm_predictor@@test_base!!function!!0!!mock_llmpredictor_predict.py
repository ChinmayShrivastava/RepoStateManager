def mock_llmpredictor_predict(prompt: BasePromptTemplate, **prompt_args: Any) -> str:
    """Mock LLMPredictor predict."""
    return prompt_args["query_str"]

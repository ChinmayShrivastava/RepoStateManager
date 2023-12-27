def patch_llmpredictor_predict(
    self: Any, prompt: BasePromptTemplate, **prompt_args: Any
) -> str:
    """Mock predict method of LLMPredictor.

    Depending on the prompt, return response.

    """
    return mock_llmpredictor_predict(prompt, **prompt_args)

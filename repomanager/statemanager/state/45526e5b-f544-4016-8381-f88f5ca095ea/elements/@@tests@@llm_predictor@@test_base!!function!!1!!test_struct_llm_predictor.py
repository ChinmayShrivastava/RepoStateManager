def test_struct_llm_predictor(mock_init: Any, mock_predict: Any) -> None:
    """Test LLM predictor."""
    llm_predictor = StructuredLLMPredictor()
    output_parser = MockOutputParser()
    prompt = PromptTemplate("{query_str}", output_parser=output_parser)
    llm_prediction = llm_predictor.predict(prompt, query_str="hello world")
    assert llm_prediction == "hello world\nhello world"

    # no change
    prompt = PromptTemplate("{query_str}")
    llm_prediction = llm_predictor.predict(prompt, query_str="hello world")
    assert llm_prediction == "hello world"

def test_tree_summarize_output_cls(
    mock_service_context_merge_chunks: ServiceContext,
) -> None:
    mock_service_context_merge_chunks.llm_predictor = LLMPredictor(MockLLM())

    mock_summary_prompt_tmpl = "{context_str}{query_str}"
    mock_summary_prompt = PromptTemplate(
        mock_summary_prompt_tmpl, prompt_type=PromptType.SUMMARY
    )

    query_str = "What is?"
    texts = [
        '{"hello":"Test Chunk 1"}',
        '{"hello":"Test Chunk 2"}',
        '{"hello":"Test Chunk 3"}',
        '{"hello":"Test Chunk 4"}',
    ]
    response_dict = {"hello": "Test Chunk 5"}

    # test sync
    tree_summarize = TreeSummarize(
        service_context=mock_service_context_merge_chunks,
        summary_template=mock_summary_prompt,
        output_cls=TestModel,
    )
    full_response = "\n".join(texts)
    response = tree_summarize.get_response(text_chunks=texts, query_str=query_str)
    assert isinstance(response, TestModel)
    assert response.dict() == response_dict

def test_tree_summarize_use_async(
    mock_service_context_merge_chunks: ServiceContext,
) -> None:
    mock_summary_prompt_tmpl = "{context_str}{query_str}"
    mock_summary_prompt = PromptTemplate(
        mock_summary_prompt_tmpl, prompt_type=PromptType.SUMMARY
    )

    query_str = "What is?"
    texts = [
        "Text chunk 1",
        "Text chunk 2",
        "Text chunk 3",
        "Text chunk 4",
    ]

    # test async
    tree_summarize = TreeSummarize(
        service_context=mock_service_context_merge_chunks,
        summary_template=mock_summary_prompt,
        use_async=True,
    )
    response = tree_summarize.get_response(text_chunks=texts, query_str=query_str)
    assert str(response) == "Text chunk 1\nText chunk 2\nText chunk 3\nText chunk 4"

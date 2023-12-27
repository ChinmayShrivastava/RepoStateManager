def test_llm_single_selector() -> None:
    service_context = ServiceContext.from_defaults(llm=None, embed_model=None)
    selector = LLMSingleSelector.from_defaults(service_context=service_context)

    with patch.object(
        type(service_context.llm),
        "complete",
        return_value=CompletionResponse(text=_mock_single_select()),
    ) as mock_complete:
        result = selector.select(
            choices=["apple", "pear", "peach"], query="what is the best fruit?"
        )
    assert result.ind == 0
    mock_complete.assert_called_once()
    assert mock_complete.call_args.args[0].count("Here is an example") <= 1

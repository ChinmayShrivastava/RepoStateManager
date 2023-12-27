def test_llm_multi_selector_max_choices(
    mock_service_context: ServiceContext,
) -> None:
    selector = LLMMultiSelector.from_defaults(
        service_context=mock_service_context, max_outputs=2
    )

    choices = [
        "apple",
        "pear",
        "peach",
    ]
    query = "what is the best fruit?"

    result = selector.select(choices, query)
    assert result.inds == [0, 1]

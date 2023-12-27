def test_completion(MockSyncOpenAI: MagicMock) -> None:
    mock_instance = MockSyncOpenAI.return_value
    mock_instance.completions.create.side_effect = [
        mock_completion("1"),
        mock_completion("2"),
    ]

    llm = OpenAILike(
        **LOCALAI_DEFAULTS, model=STUB_MODEL_NAME, context_window=1024, max_tokens=None
    )
    response = llm.complete("A long time ago in a galaxy far, far away")
    expected_calls = [
        # NOTE: has no max_tokens or tokenizer, so won't infer max_tokens
        call(
            prompt="A long time ago in a galaxy far, far away",
            stream=False,
            model=STUB_MODEL_NAME,
            temperature=0.1,
        )
    ]
    assert response.text == "1"
    mock_instance.completions.create.assert_has_calls(expected_calls)

    llm = OpenAILike(
        model=STUB_MODEL_NAME,
        context_window=1024,
        tokenizer=StubTokenizer(),
    )
    response = llm.complete("A long time ago in a galaxy far, far away")
    expected_calls += [
        # NOTE: has tokenizer, so will infer max_tokens
        call(
            prompt="A long time ago in a galaxy far, far away",
            stream=False,
            model=STUB_MODEL_NAME,
            temperature=0.1,
            max_tokens=1014,
        )
    ]
    assert response.text == "2"
    mock_instance.completions.create.assert_has_calls(expected_calls)

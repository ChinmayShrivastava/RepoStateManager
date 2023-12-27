def test_prompt_mixin() -> None:
    mock_obj1 = MockObject1()
    prompts = mock_obj1.get_prompts()
    assert prompts == {
        "summary": PromptTemplate("{summary}"),
        "foo": PromptTemplate("{foo} {bar}"),
        "mock_object_2:abc": PromptTemplate("{abc} {def}"),
    }

    assert mock_obj1.mock_object_2.get_prompts() == {
        "abc": PromptTemplate("{abc} {def}"),
    }

    # update prompts
    mock_obj1.update_prompts(
        {
            "summary": PromptTemplate("{summary} testing"),
            "mock_object_2:abc": PromptTemplate("{abc} {def} ghi"),
        }
    )
    assert mock_obj1.get_prompts() == {
        "summary": PromptTemplate("{summary} testing"),
        "foo": PromptTemplate("{foo} {bar}"),
        "mock_object_2:abc": PromptTemplate("{abc} {def} ghi"),
    }

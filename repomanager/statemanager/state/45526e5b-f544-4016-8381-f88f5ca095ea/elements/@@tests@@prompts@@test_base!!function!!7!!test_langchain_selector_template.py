def test_langchain_selector_template() -> None:
    lc_llm = FakeListLLM(responses=["test"])
    mock_llm = LangChainLLM(llm=lc_llm)

    def is_mock(llm: BaseLanguageModel) -> bool:
        return llm == lc_llm

    default_lc_template = LangchainTemplate.from_template("hello {text} {foo}")
    conditionals = [
        (is_mock, LangchainTemplate.from_template("hello {text} {foo} mock")),
    ]

    lc_selector = LangchainSelector(
        default_prompt=default_lc_template, conditionals=conditionals
    )
    template = LangchainPromptTemplate(selector=lc_selector)

    template_fmt = template.partial_format(foo="bar")
    assert isinstance(template, LangchainPromptTemplate)

    assert template_fmt.format(llm=mock_llm, text="world") == "hello world bar mock"

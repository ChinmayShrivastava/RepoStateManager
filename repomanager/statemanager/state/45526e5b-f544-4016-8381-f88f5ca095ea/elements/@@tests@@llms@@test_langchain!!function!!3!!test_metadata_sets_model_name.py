def test_metadata_sets_model_name() -> None:
    chat_gpt = LangChainLLM(
        llm=ChatOpenAI(model="gpt-4-0613", openai_api_key="model-name-tests")
    )
    assert chat_gpt.metadata.model_name == "gpt-4-0613"

    gpt35 = LangChainLLM(
        llm=OpenAI(model="gpt-3.5-turbo-0613", openai_api_key="model-name-tests")
    )
    assert gpt35.metadata.model_name == "gpt-3.5-turbo-0613"

    cohere_llm = LangChainLLM(
        llm=Cohere(model="j2-jumbo-instruct", cohere_api_key="XXXXXXX")
    )
    assert cohere_llm.metadata.model_name == "j2-jumbo-instruct"

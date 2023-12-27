def test_openai() -> None:
    llm = LiteLLM(model="gpt-3.5-turbo", api_key="")
    message = ChatMessage(role="user", content="why does LiteLLM love LlamaIndex")
    chat_response = llm.chat([message])
    print("gpt-3.5-turbo Chat response\n")
    print(chat_response)

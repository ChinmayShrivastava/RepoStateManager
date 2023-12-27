def test_tg_ai() -> None:
    # deep infra call
    llm = LiteLLM(
        model="together_ai/togethercomputer/Llama-2-7B-32K-Instruct",
        max_tokens=10,
        api_key="",
    )
    message = ChatMessage(role="user", content="why does LiteLLM love LlamaIndex")
    chat_response = llm.chat([message])
    print("\ntogetherai Chat response\n")
    print(chat_response)

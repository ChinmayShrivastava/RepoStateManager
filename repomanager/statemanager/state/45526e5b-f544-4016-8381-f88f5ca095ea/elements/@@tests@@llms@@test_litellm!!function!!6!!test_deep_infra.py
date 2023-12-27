def test_deep_infra() -> None:
    # deep infra call
    llm = LiteLLM(
        model="deepinfra/meta-llama/Llama-2-70b-chat-hf", max_tokens=10, api_key=""
    )
    message = ChatMessage(role="user", content="why does LiteLLM love LlamaIndex")
    chat_response = llm.chat([message])
    print("\ndeepinfra Chat response\n")
    print(chat_response)

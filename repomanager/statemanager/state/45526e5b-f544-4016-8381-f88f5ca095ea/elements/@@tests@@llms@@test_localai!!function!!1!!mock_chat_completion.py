def mock_chat_completion(text: str) -> ChatCompletion:
    return ChatCompletion(
        id="chatcmpl-abc123",
        object="chat.completion",
        created=1677858242,
        model="gpt-3.5-turbo-0301",
        usage={"prompt_tokens": 13, "completion_tokens": 7, "total_tokens": 20},
        choices=[
            Choice(
                message=ChatCompletionMessage(role="assistant", content=text),
                finish_reason="stop",
                index=0,
            )
        ],
    )

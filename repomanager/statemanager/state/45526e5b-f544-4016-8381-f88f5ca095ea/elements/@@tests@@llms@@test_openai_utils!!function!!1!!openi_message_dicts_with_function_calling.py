def openi_message_dicts_with_function_calling() -> List[ChatCompletionMessageParam]:
    return [
        ChatCompletionUserMessageParam(
            role="user", content="test question with functions"
        ),
        ChatCompletionAssistantMessageParam(
            role="assistant",
            content=None,
            function_call=FunctionCallParam(
                name="get_current_weather",
                arguments='{ "location": "Boston, MA"}',
            ),
        ),
        ChatCompletionFunctionMessageParam(
            role="function",
            content='{"temperature": "22", "unit": "celsius", '
            '"description": "Sunny"}',
            name="get_current_weather",
        ),
    ]

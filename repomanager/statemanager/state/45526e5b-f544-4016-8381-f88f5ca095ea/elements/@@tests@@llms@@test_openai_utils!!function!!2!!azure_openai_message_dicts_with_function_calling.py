def azure_openai_message_dicts_with_function_calling() -> List[ChatCompletionMessage]:
    """
    Taken from:
    - https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/function-calling.
    """
    return [
        ChatCompletionMessage(
            role="assistant",
            content=None,
            function_call=None,
            tool_calls=[
                ChatCompletionMessageToolCall(
                    id="0123",
                    type="function",
                    function=Function(
                        name="search_hotels",
                        arguments='{\n  "location": "San Diego",\n  "max_price": 300,\n  "features": "beachfront,free breakfast"\n}',
                    ),
                )
            ],
        )
    ]

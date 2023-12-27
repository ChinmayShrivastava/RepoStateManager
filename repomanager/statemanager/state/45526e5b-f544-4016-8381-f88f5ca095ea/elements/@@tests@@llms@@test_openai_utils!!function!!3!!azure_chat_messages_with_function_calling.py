def azure_chat_messages_with_function_calling() -> List[ChatMessage]:
    return [
        ChatMessage(
            role=MessageRole.ASSISTANT,
            content=None,
            additional_kwargs={
                "tool_calls": [
                    {
                        "id": "0123",
                        "type": "function",
                        "function": {
                            "name": "search_hotels",
                            "arguments": '{\n  "location": "San Diego",\n  "max_price": 300,\n  "features": "beachfront,free breakfast"\n}',
                        },
                    },
                ],
            },
        ),
    ]

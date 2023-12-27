def to_lc_messages(messages: Sequence[ChatMessage]) -> List[LCMessage]:
    lc_messages: List[LCMessage] = []
    for message in messages:
        if message.role == "user":
            lc_messages.append(
                HumanMessage(
                    content=message.content, additional_kwargs=message.additional_kwargs
                )
            )
        elif message.role == "assistant":
            lc_messages.append(
                AIMessage(
                    content=message.content, additional_kwargs=message.additional_kwargs
                )
            )
        elif message.role == "function":
            if "name" not in message.additional_kwargs:
                raise ValueError("name cannot be None for function message.")
            name = message.additional_kwargs.pop("name")
            lc_messages.append(
                FunctionMessage(
                    content=message.content,
                    additional_kwargs=message.additional_kwargs,
                    name=name,
                )
            )
        elif message.role == "system":
            lc_messages.append(
                SystemMessage(
                    content=message.content, additional_kwargs=message.additional_kwargs
                )
            )
        else:
            raise ValueError(f"Invalid role: {message.role}")
    return lc_messages

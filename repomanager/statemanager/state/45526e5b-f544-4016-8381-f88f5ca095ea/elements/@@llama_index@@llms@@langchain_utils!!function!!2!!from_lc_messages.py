def from_lc_messages(lc_messages: Sequence[LCMessage]) -> List[ChatMessage]:
    messages: List[ChatMessage] = []
    for lc_message in lc_messages:
        if isinstance(lc_message, HumanMessage):
            messages.append(
                ChatMessage(
                    content=lc_message.content,
                    additional_kwargs=lc_message.additional_kwargs,
                    role=MessageRole.USER,
                )
            )
        elif isinstance(lc_message, AIMessage):
            messages.append(
                ChatMessage(
                    content=lc_message.content,
                    additional_kwargs=lc_message.additional_kwargs,
                    role=MessageRole.ASSISTANT,
                )
            )
        elif isinstance(lc_message, FunctionMessage):
            messages.append(
                ChatMessage(
                    content=lc_message.content,
                    additional_kwargs=lc_message.additional_kwargs,
                    name=lc_message.name,
                    role=MessageRole.FUNCTION,
                )
            )
        elif isinstance(lc_message, SystemMessage):
            messages.append(
                ChatMessage(
                    content=lc_message.content,
                    additional_kwargs=lc_message.additional_kwargs,
                    role=MessageRole.SYSTEM,
                )
            )
        else:
            raise ValueError(f"Invalid message type: {type(lc_message)}")
    return messages

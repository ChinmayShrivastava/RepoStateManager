def chat_messages_to_conversational_kwargs(
    messages: Sequence[ChatMessage],
) -> Dict[str, Any]:
    """Convert ChatMessages to keyword arguments for Inference API conversational."""
    if len(messages) % 2 != 1:
        raise NotImplementedError("Messages passed in must be of odd length.")
    last_message = messages[-1]
    kwargs: Dict[str, Any] = {
        "text": last_message.content,
        **last_message.additional_kwargs,
    }
    if len(messages) != 1:
        kwargs["past_user_inputs"] = []
        kwargs["generated_responses"] = []
        for user_msg, assistant_msg in zip(messages[::2], messages[1::2]):
            if (
                user_msg.role != MessageRole.USER
                or assistant_msg.role != MessageRole.ASSISTANT
            ):
                raise NotImplementedError(
                    "Didn't handle when messages aren't ordered in alternating"
                    f" pairs of {(MessageRole.USER, MessageRole.ASSISTANT)}."
                )
            kwargs["past_user_inputs"].append(user_msg.content)
            kwargs["generated_responses"].append(assistant_msg.content)
    return kwargs

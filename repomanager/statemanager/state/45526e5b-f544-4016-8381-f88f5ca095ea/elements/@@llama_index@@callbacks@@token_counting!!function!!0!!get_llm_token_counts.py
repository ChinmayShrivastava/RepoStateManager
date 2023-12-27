def get_llm_token_counts(
    token_counter: TokenCounter, payload: Dict[str, Any], event_id: str = ""
) -> TokenCountingEvent:
    from llama_index.llms import ChatMessage

    if EventPayload.PROMPT in payload:
        prompt = str(payload.get(EventPayload.PROMPT))
        completion = str(payload.get(EventPayload.COMPLETION))

        return TokenCountingEvent(
            event_id=event_id,
            prompt=prompt,
            prompt_token_count=token_counter.get_string_tokens(prompt),
            completion=completion,
            completion_token_count=token_counter.get_string_tokens(completion),
        )

    elif EventPayload.MESSAGES in payload:
        messages = cast(List[ChatMessage], payload.get(EventPayload.MESSAGES, []))
        messages_str = "\n".join([str(x) for x in messages])

        response = payload.get(EventPayload.RESPONSE)
        response_str = str(response)

        # try getting attached token counts first
        try:
            messages_tokens = 0
            response_tokens = 0

            if response is not None and response.raw is not None:
                usage = response.raw.get("usage")  # type: ignore

                if usage is not None:
                    messages_tokens = usage.get("prompt_tokens", 0)
                    response_tokens = usage.get("completion_tokens", 0)

                if messages_tokens == 0 or response_tokens == 0:
                    raise ValueError("Invalid token counts!")

                return TokenCountingEvent(
                    event_id=event_id,
                    prompt=messages_str,
                    prompt_token_count=messages_tokens,
                    completion=response_str,
                    completion_token_count=response_tokens,
                )

        except (ValueError, KeyError):
            # Invalid token counts, or no token counts attached
            pass

        # Should count tokens ourselves
        messages_tokens = token_counter.estimate_tokens_in_messages(messages)
        response_tokens = token_counter.get_string_tokens(response_str)

        return TokenCountingEvent(
            event_id=event_id,
            prompt=messages_str,
            prompt_token_count=messages_tokens,
            completion=response_str,
            completion_token_count=response_tokens,
        )
    else:
        raise ValueError(
            "Invalid payload! Need prompt and completion or messages and response."
        )

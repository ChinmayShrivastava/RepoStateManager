                    def wrapped_gen() -> ChatResponseGen:
                        last_response = None
                        for x in f_return_val:
                            yield cast(ChatResponse, x)
                            last_response = x

                        callback_manager.on_event_end(
                            CBEventType.LLM,
                            payload={
                                EventPayload.MESSAGES: messages,
                                EventPayload.RESPONSE: last_response,
                            },
                            event_id=event_id,
                        )

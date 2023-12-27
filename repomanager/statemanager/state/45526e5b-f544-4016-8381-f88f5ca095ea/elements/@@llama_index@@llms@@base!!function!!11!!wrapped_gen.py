                    def wrapped_gen() -> CompletionResponseGen:
                        last_response = None
                        for x in f_return_val:
                            yield cast(CompletionResponse, x)
                            last_response = x

                        callback_manager.on_event_end(
                            CBEventType.LLM,
                            payload={
                                EventPayload.PROMPT: args[0],
                                EventPayload.COMPLETION: last_response,
                            },
                            event_id=event_id,
                        )

        def wrapped_llm_predict(_self: Any, *args: Any, **kwargs: Any) -> Any:
            with wrapper_logic(_self) as callback_manager:
                event_id = callback_manager.on_event_start(
                    CBEventType.LLM,
                    payload={
                        EventPayload.PROMPT: args[0],
                        EventPayload.ADDITIONAL_KWARGS: kwargs,
                        EventPayload.SERIALIZED: _self.to_dict(),
                    },
                )

                f_return_val = f(_self, *args, **kwargs)
                if isinstance(f_return_val, Generator):
                    # intercept the generator and add a callback to the end
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

                    return wrapped_gen()
                else:
                    callback_manager.on_event_end(
                        CBEventType.LLM,
                        payload={
                            EventPayload.PROMPT: args[0],
                            EventPayload.COMPLETION: f_return_val,
                        },
                        event_id=event_id,
                    )

            return f_return_val

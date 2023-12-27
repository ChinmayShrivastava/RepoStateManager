    def gen() -> CompletionResponseGen:
        for response in chat_response_gen:
            yield CompletionResponse(
                text=response.message.content or "",
                additional_kwargs=response.message.additional_kwargs,
                delta=response.delta,
                raw=response.raw,
            )

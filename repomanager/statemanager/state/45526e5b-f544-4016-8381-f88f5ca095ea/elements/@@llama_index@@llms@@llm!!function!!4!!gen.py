    def gen() -> TokenGen:
        for response in chat_response_gen:
            yield response.delta or ""

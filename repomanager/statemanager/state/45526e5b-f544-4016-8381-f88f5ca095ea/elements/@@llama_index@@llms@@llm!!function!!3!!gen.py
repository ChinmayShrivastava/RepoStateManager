    def gen() -> TokenGen:
        for response in completion_response_gen:
            yield response.delta or ""

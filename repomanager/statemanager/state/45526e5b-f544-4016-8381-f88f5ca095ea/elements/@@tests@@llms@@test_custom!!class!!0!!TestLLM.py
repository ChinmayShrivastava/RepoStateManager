class TestLLM(CustomLLM):
    __test__ = False

    def __init__(self) -> None:
        super().__init__(callback_manager=None)

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata()

    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        return CompletionResponse(
            text="test output",
            additional_kwargs={
                "prompt": prompt,
            },
        )

    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        def gen() -> CompletionResponseGen:
            text = "test output"
            text_so_far = ""
            for ch in text:
                text_so_far += ch
                yield CompletionResponse(
                    text=text_so_far,
                    delta=ch,
                    additional_kwargs={
                        "prompt": prompt,
                    },
                )

        return gen()

class MockGenaiPackage(mock.Mock):
    """Stubbed-out google.generativeai package."""

    response_text = "default response"

    def get_model(self, name: str, **kwargs: Any) -> Any:
        model = mock.Mock()
        model.name = name
        model.supported_generation_methods = ["generateContent"]
        model.input_token_limit = 4321
        model.output_token_limit = 12345
        return model

    def _gen_content(
        self, contents: Any, *, stream: bool = False, **kwargs: Any
    ) -> Any:
        content = mock.Mock()
        content.text = self.response_text
        content.candidates = [
            FakeGoogleDataclass(
                {
                    "content": {
                        "parts": [{"text": self.response_text}],
                        "role": "model",
                    },
                    "finish_reason": 1,
                }
            )
        ]
        content.prompt_feedback = FakeGoogleDataclass({})

        if stream:
            # Can't yield-from here as this function is called as a mock side effect.
            return [content]
        else:
            return content

    def GenerativeModel(self, **kwargs: Any) -> Any:
        gmodel = mock.Mock()
        gmodel.generate_content.side_effect = self._gen_content
        return gmodel

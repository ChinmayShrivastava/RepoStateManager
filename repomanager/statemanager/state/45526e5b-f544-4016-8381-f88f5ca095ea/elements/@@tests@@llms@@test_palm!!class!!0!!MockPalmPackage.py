class MockPalmPackage(MagicMock):
    """Mock PaLM package."""

    def _mock_models(self) -> Any:
        model = MagicMock()
        model.name = "palm_model"
        return [model]

    def generate_text(self, model: str, prompt: str, **kwargs: Any) -> str:
        """Mock PaLM completion."""
        return _mock_palm_completion(model, prompt, **kwargs)

    def list_models(self) -> Any:
        return self._mock_models()

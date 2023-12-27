class MockGradient(MagicMock):
    """Mock Gradient package."""

    def get_base_model(self, base_model_slug: str) -> GradientModel:
        assert base_model_slug == "dummy-base-model"

        return GradientModel()

    def close(self) -> None:
        """Mock Gradient completion."""
        return

    def get_model_adapter(self, model_adapter_id: str) -> GradientModel:
        assert model_adapter_id == "dummy-adapter-model"
        return GradientModel()

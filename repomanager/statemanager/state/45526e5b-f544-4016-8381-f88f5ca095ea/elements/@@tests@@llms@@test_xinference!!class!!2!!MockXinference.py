class MockXinference(Xinference):
    def load_model(
        self,
        model_uid: str,
        endpoint: str,
    ) -> Tuple[Any, int, Dict[Any, Any]]:
        client = MockRESTfulClient()  # type: ignore[assignment]

        assert client is not None
        generator = client.get_model()

        return generator, 256, {}

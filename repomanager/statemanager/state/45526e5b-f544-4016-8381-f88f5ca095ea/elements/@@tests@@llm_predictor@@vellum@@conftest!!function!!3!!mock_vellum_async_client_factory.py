def mock_vellum_async_client_factory() -> Callable[..., mock.MagicMock]:
    def _create_async_vellum_client() -> mock.MagicMock:
        return mock.MagicMock()

    return _create_async_vellum_client

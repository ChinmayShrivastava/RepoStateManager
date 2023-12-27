def test_set_google_config(mock_credentials: MagicMock) -> None:
    set_google_config(auth_credentials=mock_credentials)
    config = genaix.get_config()
    assert config.auth_credentials == mock_credentials

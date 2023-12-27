def mock_openai_credentials() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "sk-" + ("a" * 48)

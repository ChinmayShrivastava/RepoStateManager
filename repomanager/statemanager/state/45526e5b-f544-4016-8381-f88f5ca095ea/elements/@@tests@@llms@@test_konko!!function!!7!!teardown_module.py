def teardown_module() -> None:
    import os

    del os.environ["KONKO_API_KEY"]

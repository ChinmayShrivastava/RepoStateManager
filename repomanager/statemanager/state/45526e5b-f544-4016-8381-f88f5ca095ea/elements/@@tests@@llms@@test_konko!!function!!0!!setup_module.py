def setup_module() -> None:
    import os

    os.environ["KONKO_API_KEY"] = "ko-" + "a" * 48

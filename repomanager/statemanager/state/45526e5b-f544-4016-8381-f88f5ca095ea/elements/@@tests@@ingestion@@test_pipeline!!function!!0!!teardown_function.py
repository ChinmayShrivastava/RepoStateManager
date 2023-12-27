def teardown_function() -> None:
    import shutil

    shutil.rmtree("./test_pipeline", ignore_errors=True)

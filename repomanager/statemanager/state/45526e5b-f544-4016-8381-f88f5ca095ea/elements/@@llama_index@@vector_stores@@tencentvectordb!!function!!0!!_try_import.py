def _try_import() -> None:
    try:
        import tcvectordb  # noqa
    except ImportError:
        raise ImportError(
            "`tcvectordb` package not found, please run `pip install tcvectordb`"
        )

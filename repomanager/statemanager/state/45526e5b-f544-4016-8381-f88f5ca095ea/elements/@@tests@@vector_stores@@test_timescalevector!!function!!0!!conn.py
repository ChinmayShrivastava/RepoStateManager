def conn() -> Any:
    import psycopg2

    return psycopg2.connect(TEST_SERVICE_URL)  # type: ignore

def conn() -> Any:
    import psycopg2

    return psycopg2.connect(**PARAMS)  # type: ignore

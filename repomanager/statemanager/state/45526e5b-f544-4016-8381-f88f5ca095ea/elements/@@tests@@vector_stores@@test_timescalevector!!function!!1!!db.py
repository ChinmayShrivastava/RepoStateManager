def db(conn: Any) -> Generator:
    conn.autocommit = True

    with conn.cursor() as c:
        c.execute(f"DROP TABLE IF EXISTS {TEST_TABLE_NAME}")
        conn.commit()
    yield
    with conn.cursor() as c:
        # c.execute(f"DROP TABLE IF EXISTS {TEST_TABLE_NAME}")
        conn.commit()

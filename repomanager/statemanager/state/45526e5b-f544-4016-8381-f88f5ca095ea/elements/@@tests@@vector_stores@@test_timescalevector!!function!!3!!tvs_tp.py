def tvs_tp(db: None) -> Any:
    tvs = TimescaleVectorStore.from_params(
        service_url=TEST_SERVICE_URL,
        table_name=TEST_TABLE_NAME,
        time_partition_interval=timedelta(hours=1),
    )

    yield tvs

    try:
        asyncio.get_event_loop().run_until_complete(tvs.close())
    except RuntimeError:
        asyncio.run(tvs.close())

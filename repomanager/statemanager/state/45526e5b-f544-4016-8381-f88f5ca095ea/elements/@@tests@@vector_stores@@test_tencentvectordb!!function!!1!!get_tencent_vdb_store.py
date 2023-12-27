def get_tencent_vdb_store(drop_exists: bool = False) -> TencentVectorDB:
    filter_fields = [
        FilterField(name="author"),
        FilterField(name="age", data_type="uint64"),
    ]

    return TencentVectorDB(
        url="http://10.0.X.X",
        key="eC4bLRy2va******************************",
        collection_params=CollectionParams(
            dimension=2, drop_exists=drop_exists, filter_fields=filter_fields
        ),
    )

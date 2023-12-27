def tool(mock_service_context: ServiceContext) -> OnDemandLoaderTool:
    # import most basic string reader
    reader = StringIterableReader()
    return OnDemandLoaderTool.from_defaults(
        reader=reader,
        index_cls=VectorStoreIndex,
        index_kwargs={"service_context": mock_service_context},
        name="ondemand_loader_tool",
        description="ondemand_loader_tool_desc",
        fn_schema=TestSchemaSpec,
    )

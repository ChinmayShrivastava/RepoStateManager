def embedded_milvus() -> Generator:
    default_server.cleanup()
    default_server.start()
    yield "http://" + str(default_server.server_address) + ":" + str(
        default_server.listen_port
    )
    default_server.stop()
    default_server.cleanup()

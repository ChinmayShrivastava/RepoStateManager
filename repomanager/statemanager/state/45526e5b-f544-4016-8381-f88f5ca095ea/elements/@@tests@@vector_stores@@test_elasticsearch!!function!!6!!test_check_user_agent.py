def test_check_user_agent(
    index_name: str,
    node_embeddings: List[TextNode],
) -> None:
    from elastic_transport import AsyncTransport
    from elasticsearch import AsyncElasticsearch

    class CustomTransport(AsyncTransport):
        requests = []

        async def perform_request(self, *args, **kwargs):  # type: ignore
            self.requests.append(kwargs)
            return await super().perform_request(*args, **kwargs)

    es_client_instance = AsyncElasticsearch(
        "http://localhost:9200",
        transport_class=CustomTransport,
    )

    es_store = ElasticsearchStore(
        es_client=es_client_instance,
        index_name=index_name,
        distance_strategy="EUCLIDEAN_DISTANCE",
    )

    es_store.add(node_embeddings)

    user_agent = es_client_instance.transport.requests[0]["headers"][  # type: ignore
        "user-agent"
    ]
    pattern = r"^llama_index-py-vs/\d+\.\d+\.\d+$"
    match = re.match(pattern, user_agent)

    assert (
        match is not None
    ), f"The string '{user_agent}' does not match the expected user-agent."

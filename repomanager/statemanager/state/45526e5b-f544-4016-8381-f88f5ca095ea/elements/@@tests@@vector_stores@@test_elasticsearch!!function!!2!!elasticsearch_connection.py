def elasticsearch_connection() -> Union[dict, Generator[dict, None, None]]:
    # Running this integration test with Elastic Cloud
    # Required for in-stack inference testing (ELSER + model_id)
    from elasticsearch import Elasticsearch

    es_url = os.environ.get("ES_URL", "http://localhost:9200")
    cloud_id = os.environ.get("ES_CLOUD_ID")
    es_username = os.environ.get("ES_USERNAME", "elastic")
    es_password = os.environ.get("ES_PASSWORD", "changeme")

    if cloud_id:
        yield {
            "es_cloud_id": cloud_id,
            "es_user": es_username,
            "es_password": es_password,
        }
        es = Elasticsearch(cloud_id=cloud_id, basic_auth=(es_username, es_password))

    else:
        # Running this integration test with local docker instance
        yield {
            "es_url": es_url,
        }
        es = Elasticsearch(hosts=es_url)

    # Clear all indexes
    index_names = es.indices.get(index="_all").keys()
    for index_name in index_names:
        if index_name.startswith("test_"):
            es.indices.delete(index=index_name)
    es.indices.refresh(index="_all")

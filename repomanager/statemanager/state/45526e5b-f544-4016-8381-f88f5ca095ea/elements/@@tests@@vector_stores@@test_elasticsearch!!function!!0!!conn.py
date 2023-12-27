def conn() -> Any:
    import elasticsearch

    return elasticsearch.Elasticsearch("http://localhost:9200")

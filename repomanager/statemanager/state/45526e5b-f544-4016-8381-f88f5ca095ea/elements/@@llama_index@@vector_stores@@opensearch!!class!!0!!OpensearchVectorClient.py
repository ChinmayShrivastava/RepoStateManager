class OpensearchVectorClient:
    """Object encapsulating an Opensearch index that has vector search enabled.

    If the index does not yet exist, it is created during init.
    Therefore, the underlying index is assumed to either:
    1) not exist yet or 2) be created due to previous usage of this class.

    Args:
        endpoint (str): URL (http/https) of elasticsearch endpoint
        index (str): Name of the elasticsearch index
        dim (int): Dimension of the vector
        embedding_field (str): Name of the field in the index to store
            embedding array in.
        text_field (str): Name of the field to grab text from
        method (Optional[dict]): Opensearch "method" JSON obj for configuring
            the KNN index.
            This includes engine, metric, and other config params. Defaults to:
            {"name": "hnsw", "space_type": "l2", "engine": "faiss",
            "parameters": {"ef_construction": 256, "m": 48}}
        **kwargs: Optional arguments passed to the OpenSearch client from opensearch-py.

    """

    def __init__(
        self,
        endpoint: str,
        index: str,
        dim: int,
        embedding_field: str = "embedding",
        text_field: str = "content",
        method: Optional[dict] = None,
        max_chunk_bytes: int = 1 * 1024 * 1024,
        search_pipeline: Optional[str] = None,
        **kwargs: Any,
    ):
        """Init params."""
        if method is None:
            method = {
                "name": "hnsw",
                "space_type": "l2",
                "engine": "nmslib",
                "parameters": {"ef_construction": 256, "m": 48},
            }
        if embedding_field is None:
            embedding_field = "embedding"
        self._embedding_field = embedding_field

        self._endpoint = endpoint
        self._dim = dim
        self._index = index
        self._text_field = text_field
        self._max_chunk_bytes = max_chunk_bytes

        self._search_pipeline = search_pipeline
        # initialize mapping
        idx_conf = {
            "settings": {"index": {"knn": True, "knn.algo_param.ef_search": 100}},
            "mappings": {
                "properties": {
                    embedding_field: {
                        "type": "knn_vector",
                        "dimension": dim,
                        "method": method,
                    },
                }
            },
        }
        self._os_client = _get_opensearch_client(self._endpoint, **kwargs)
        not_found_error = _import_not_found_error()
        try:
            self._os_client.indices.get(index=self._index)
        except not_found_error:
            self._os_client.indices.create(index=self._index, body=idx_conf)
            self._os_client.indices.refresh(index=self._index)

    def index_results(self, nodes: List[BaseNode], **kwargs: Any) -> List[str]:
        """Store results in the index."""
        embeddings: List[List[float]] = []
        texts: List[str] = []
        metadatas: List[dict] = []
        ids: List[str] = []
        for node in nodes:
            ids.append(node.node_id)
            embeddings.append(node.get_embedding())
            texts.append(node.get_content(metadata_mode=MetadataMode.NONE))
            metadatas.append(node_to_metadata_dict(node, remove_text=True))

        return _bulk_ingest_embeddings(
            self._os_client,
            self._index,
            embeddings,
            texts,
            metadatas=metadatas,
            ids=ids,
            vector_field=self._embedding_field,
            text_field=self._text_field,
            mapping=None,
            max_chunk_bytes=self._max_chunk_bytes,
        )

    def delete_doc_id(self, doc_id: str) -> None:
        """Delete a document.

        Args:
            doc_id (str): document id
        """
        self._os_client.delete(index=self._index, id=doc_id)

    def query(
        self,
        query_mode: VectorStoreQueryMode,
        query_str: Optional[str],
        query_embedding: List[float],
        k: int,
        filters: Optional[MetadataFilters] = None,
    ) -> VectorStoreQueryResult:
        if query_mode == VectorStoreQueryMode.HYBRID:
            if query_str is None or self._search_pipeline is None:
                raise ValueError(INVALID_HYBRID_QUERY_ERROR)
            search_query = _hybrid_search_query(
                self._text_field,
                query_str,
                self._embedding_field,
                query_embedding,
                k,
                filters=filters,
            )
            params = {"search_pipeline": self._search_pipeline}
        else:
            search_query = _knn_search_query(
                self._embedding_field, query_embedding, k, filters=filters
            )
            params = None

        res = self._os_client.search(
            index=self._index, body=search_query, params=params
        )
        nodes = []
        ids = []
        scores = []
        for hit in res["hits"]["hits"]:
            source = hit["_source"]
            node_id = hit["_id"]
            text = source[self._text_field]
            metadata = source.get("metadata", None)

            try:
                node = metadata_dict_to_node(metadata)
                node.text = text
            except Exception:
                # TODO: Legacy support for old nodes
                node_info = source.get("node_info")
                relationships = source.get("relationships") or {}
                start_char_idx = None
                end_char_idx = None
                if isinstance(node_info, dict):
                    start_char_idx = node_info.get("start", None)
                    end_char_idx = node_info.get("end", None)

                node = TextNode(
                    text=text,
                    metadata=metadata,
                    id_=node_id,
                    start_char_idx=start_char_idx,
                    end_char_idx=end_char_idx,
                    relationships=relationships,
                    extra_info=source,
                )
            ids.append(node_id)
            nodes.append(node)
            scores.append(hit["_score"])
        return VectorStoreQueryResult(nodes=nodes, ids=ids, similarities=scores)

class CollectionParams:
    r"""Tencent vector DB Collection params.
    See the following documentation for details:
    https://cloud.tencent.com/document/product/1709/95826.

    Args:
        dimension int: The dimension of vector.
        shard int: The number of shards in the collection.
        replicas int: The number of replicas in the collection.
        index_type (Optional[str]): HNSW, IVF_FLAT, IVF_PQ, IVF_SQ8... Default value is "HNSW"
        metric_type (Optional[str]): L2, COSINE, IP. Default value is "COSINE"
        drop_exists (Optional[bool]): Delete the existing Collection. Default value is False.
        vector_params (Optional[Dict]):
          if HNSW set parameters: `M` and `efConstruction`, for example `{'M': 16, efConstruction: 200}`
          if IVF_FLAT or IVF_SQ8 set parameter: `nlist`
          if IVF_PQ set parameters: `M` and `nlist`
          default is HNSW
        filter_fields: Optional[List[FilterField]]: Set the fields for filtering
          for example: [FilterField(name='author'), FilterField(name='age', data_type=uint64)]
          This can be used when calling the query method：
             store.add([
                TextNode(..., metadata={'age'=23, 'name'='name1'})
            ])
             ...
             query = VectorStoreQuery(...)
             store.query(query, filter="age > 20 and age < 40 and name in (\"name1\", \"name2\")")
    """

    def __init__(
        self,
        dimension: int,
        collection_name: str = DEFAULT_COLLECTION_NAME,
        collection_description: str = DEFAULT_COLLECTION_DESC,
        shard: int = DEFAULT_SHARD,
        replicas: int = DEFAULT_REPLICAS,
        index_type: str = DEFAULT_INDEX_TYPE,
        metric_type: str = DEFAULT_METRIC_TYPE,
        drop_exists: Optional[bool] = False,
        vector_params: Optional[Dict] = None,
        filter_fields: Optional[List[FilterField]] = [],
    ):
        self.collection_name = collection_name
        self.collection_description = collection_description
        self.dimension = dimension
        self.shard = shard
        self.replicas = replicas
        self.index_type = index_type
        self.metric_type = metric_type
        self.vector_params = vector_params
        self.drop_exists = drop_exists
        self.filter_fields = filter_fields or []

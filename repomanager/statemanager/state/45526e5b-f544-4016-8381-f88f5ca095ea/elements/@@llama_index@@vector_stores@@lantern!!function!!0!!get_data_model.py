def get_data_model(
    base: Type,
    index_name: str,
    schema_name: str,
    hybrid_search: bool,
    text_search_config: str,
    cache_okay: bool,
    embed_dim: int = 1536,
    m: int = 16,
    ef_construction: int = 128,
    ef: int = 64,
) -> Any:
    """
    This part create a dynamic sqlalchemy model with a new table.
    """
    from sqlalchemy import Column, Computed
    from sqlalchemy.dialects.postgresql import (
        ARRAY,
        BIGINT,
        JSON,
        REAL,
        TSVECTOR,
        VARCHAR,
    )
    from sqlalchemy.schema import Index
    from sqlalchemy.types import TypeDecorator

    class TSVector(TypeDecorator):
        impl = TSVECTOR
        cache_ok = cache_okay

    tablename = "data_%s" % index_name  # dynamic table name
    class_name = "Data%s" % index_name  # dynamic class name
    indexname = "%s_idx" % index_name  # dynamic index name
    hnsw_indexname = "%s_hnsw_idx" % index_name  # dynamic hnsw index name

    if hybrid_search:

        class HybridAbstractData(base):  # type: ignore
            __abstract__ = True  # this line is necessary
            id = Column(BIGINT, primary_key=True, autoincrement=True)
            text = Column(VARCHAR, nullable=False)
            metadata_ = Column(JSON)
            node_id = Column(VARCHAR)
            embedding = Column(ARRAY(REAL, embed_dim))  # type: ignore
            text_search_tsv = Column(  # type: ignore
                TSVector(),
                Computed(
                    "to_tsvector('%s', text)" % text_search_config, persisted=True
                ),
            )

        model = type(
            class_name,
            (HybridAbstractData,),
            {"__tablename__": tablename, "__table_args__": {"schema": schema_name}},
        )

        Index(
            indexname,
            model.text_search_tsv,  # type: ignore
            postgresql_using="gin",
        )
    else:

        class AbstractData(base):  # type: ignore
            __abstract__ = True  # this line is necessary
            id = Column(BIGINT, primary_key=True, autoincrement=True)
            text = Column(VARCHAR, nullable=False)
            metadata_ = Column(JSON)
            node_id = Column(VARCHAR)
            embedding = Column(ARRAY(REAL, embed_dim))  # type: ignore

        model = type(
            class_name,
            (AbstractData,),
            {"__tablename__": tablename, "__table_args__": {"schema": schema_name}},
        )

    Index(
        hnsw_indexname,
        model.embedding,  # type: ignore
        postgresql_using="hnsw",
        postgresql_with={
            "m": m,
            "ef_construction": ef_construction,
            "ef": ef,
            "dim": embed_dim,
        },
        postgresql_ops={"embedding": "dist_cos_ops"},
    )
    return model

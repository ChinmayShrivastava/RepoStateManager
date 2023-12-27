def get_data_model(
    base: Type,
    index_name: str,
    schema_name: str,
    hybrid_search: bool,
    text_search_config: str,
    cache_okay: bool,
    embed_dim: int = 1536,
    use_jsonb: bool = False,
) -> Any:
    """
    This part create a dynamic sqlalchemy model with a new table.
    """
    from pgvector.sqlalchemy import Vector
    from sqlalchemy import Column, Computed
    from sqlalchemy.dialects.postgresql import BIGINT, JSON, JSONB, TSVECTOR, VARCHAR
    from sqlalchemy.schema import Index
    from sqlalchemy.types import TypeDecorator

    class TSVector(TypeDecorator):
        impl = TSVECTOR
        cache_ok = cache_okay

    tablename = "data_%s" % index_name  # dynamic table name
    class_name = "Data%s" % index_name  # dynamic class name
    indexname = "%s_idx" % index_name  # dynamic class name

    metadata_dtype = JSONB if use_jsonb else JSON

    if hybrid_search:

        class HybridAbstractData(base):  # type: ignore
            __abstract__ = True  # this line is necessary
            id = Column(BIGINT, primary_key=True, autoincrement=True)
            text = Column(VARCHAR, nullable=False)
            metadata_ = Column(metadata_dtype)
            node_id = Column(VARCHAR)
            embedding = Column(Vector(embed_dim))  # type: ignore
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
            metadata_ = Column(metadata_dtype)
            node_id = Column(VARCHAR)
            embedding = Column(Vector(embed_dim))  # type: ignore

        model = type(
            class_name,
            (AbstractData,),
            {"__tablename__": tablename, "__table_args__": {"schema": schema_name}},
        )

    return model

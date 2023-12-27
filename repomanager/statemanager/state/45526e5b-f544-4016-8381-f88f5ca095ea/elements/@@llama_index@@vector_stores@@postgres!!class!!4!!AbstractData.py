        class AbstractData(base):  # type: ignore
            __abstract__ = True  # this line is necessary
            id = Column(BIGINT, primary_key=True, autoincrement=True)
            text = Column(VARCHAR, nullable=False)
            metadata_ = Column(metadata_dtype)
            node_id = Column(VARCHAR)
            embedding = Column(Vector(embed_dim))  # type: ignore

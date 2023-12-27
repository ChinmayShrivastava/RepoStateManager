        class AbstractData(base):  # type: ignore
            __abstract__ = True  # this line is necessary
            id = Column(BIGINT, primary_key=True, autoincrement=True)
            text = Column(VARCHAR, nullable=False)
            metadata_ = Column(JSON)
            node_id = Column(VARCHAR)
            embedding = Column(ARRAY(REAL, embed_dim))  # type: ignore

class VectorStoreType(str, Enum):
    SIMPLE = "simple"
    REDIS = "redis"
    WEAVIATE = "weaviate"
    QDRANT = "qdrant"
    PINECONE = "pinecone"
    OPENSEARCH = "opensearch"
    FAISS = "faiss"
    CASSANDRA = "cassandra"
    CHROMA = "chroma"
    CHATGPT_PLUGIN = "chatgpt_plugin"
    LANCEDB = "lancedb"
    MILVUS = "milvus"
    DEEPLAKE = "deeplake"
    MYSCALE = "myscale"
    SUPABASE = "supabase"
    ROCKSET = "rockset"
    BAGEL = "bagel"
    EPSILLA = "epsilla"
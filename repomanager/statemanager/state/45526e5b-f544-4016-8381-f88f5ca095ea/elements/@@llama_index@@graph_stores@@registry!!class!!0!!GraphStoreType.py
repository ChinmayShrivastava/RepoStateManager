class GraphStoreType(str, Enum):
    SIMPLE = "simple_kg"
    NEBULA = "nebulagraph"
    KUZU = "kuzu"
    NEO4J = "neo4j"
    FALKORDB = "falkordb"

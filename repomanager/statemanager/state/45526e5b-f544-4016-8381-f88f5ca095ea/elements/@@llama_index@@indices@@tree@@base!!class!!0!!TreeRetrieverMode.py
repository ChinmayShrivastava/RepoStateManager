class TreeRetrieverMode(str, Enum):
    SELECT_LEAF = "select_leaf"
    SELECT_LEAF_EMBEDDING = "select_leaf_embedding"
    ALL_LEAF = "all_leaf"
    ROOT = "root"

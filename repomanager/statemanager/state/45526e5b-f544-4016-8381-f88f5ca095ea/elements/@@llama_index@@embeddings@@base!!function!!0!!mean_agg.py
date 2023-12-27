def mean_agg(embeddings: List[Embedding]) -> Embedding:
    """Mean aggregation for embeddings."""
    return list(np.array(embeddings).mean(axis=0))

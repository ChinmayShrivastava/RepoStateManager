def get_top_k_mmr_embeddings(
    query_embedding: List[float],
    embeddings: List[List[float]],
    similarity_fn: Optional[Callable[..., float]] = None,
    similarity_top_k: Optional[int] = None,
    embedding_ids: Optional[List] = None,
    similarity_cutoff: Optional[float] = None,
    mmr_threshold: Optional[float] = None,
) -> Tuple[List[float], List]:
    """Get top nodes by similarity to the query,
    discount by their similarity to previous results.

    A mmr_threshold of 0 will strongly avoid similarity to previous results.
    A mmr_threshold of 1 will check similarity the query and ignore previous results.

    """
    threshold = mmr_threshold or 0.5
    similarity_fn = similarity_fn or default_similarity_fn

    if embedding_ids is None or embedding_ids == []:
        embedding_ids = list(range(len(embeddings)))
    full_embed_map = dict(zip(embedding_ids, range(len(embedding_ids))))
    embed_map = full_embed_map.copy()
    embed_similarity = {}
    score: float = -math.inf
    high_score_id = None

    for i, emb in enumerate(embeddings):
        similarity = similarity_fn(query_embedding, emb)
        embed_similarity[embedding_ids[i]] = similarity
        if similarity * threshold > score:
            high_score_id = embedding_ids[i]
            score = similarity * threshold

    results: List[Tuple[Any, Any]] = []

    embedding_length = len(embeddings or [])
    similarity_top_k_count = similarity_top_k or embedding_length
    while len(results) < min(similarity_top_k_count, embedding_length):
        # Calculate the similarity score the for the leading one.
        results.append((score, high_score_id))

        # Reset so a new high scoring result can be found
        del embed_map[high_score_id]
        recent_embedding_id = high_score_id
        score = -math.inf

        # Iterate through results to find high score
        for embed_id in embed_map:
            overlap_with_recent = similarity_fn(
                embeddings[embed_map[embed_id]],
                embeddings[full_embed_map[recent_embedding_id]],
            )
            if (
                threshold * embed_similarity[embed_id]
                - ((1 - threshold) * overlap_with_recent)
                > score
            ):
                score = threshold * embed_similarity[embed_id] - (
                    (1 - threshold) * overlap_with_recent
                )
                high_score_id = embed_id

    result_similarities = [s for s, _ in results]
    result_ids = [n for _, n in results]

    return result_similarities, result_ids

def vector_search(
    query_vector: Union[List, np.ndarray],
    data_vectors: np.ndarray,
    distance_metric: str = "l2",
    limit: Optional[int] = 4,
) -> List:
    """Naive search for nearest neighbors
    args:
        query_vector: Union[List, np.ndarray]
        data_vectors: np.ndarray
        limit (int): number of nearest neighbors
        distance_metric: distance function 'L2' for Euclidean, 'L1' for Nuclear, 'Max'
            l-infinity distance, 'cos' for cosine similarity, 'dot' for dot product
    returns:
        nearest_indices: List, indices of nearest neighbors.
    """
    # Calculate the distance between the query_vector and all data_vectors
    if isinstance(query_vector, list):
        query_vector = np.array(query_vector)
        query_vector = query_vector.reshape(1, -1)

    distances = distance_metric_map[distance_metric](query_vector, data_vectors)
    nearest_indices = np.argsort(distances)

    nearest_indices = (
        nearest_indices[::-1][:limit]
        if distance_metric in ["cos"]
        else nearest_indices[:limit]
    )

    return nearest_indices.tolist()

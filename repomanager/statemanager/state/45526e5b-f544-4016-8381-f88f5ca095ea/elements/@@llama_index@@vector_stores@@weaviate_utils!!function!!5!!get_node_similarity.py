def get_node_similarity(entry: Dict, similarity_key: str = "distance") -> float:
    """Get converted node similarity from distance."""
    distance = entry["_additional"].get(similarity_key, 0.0)

    if distance is None:
        return 1.0

    # convert distance https://forum.weaviate.io/t/distance-vs-certainty-scores/258
    return 1.0 - float(distance)

def _to_llama_similarities(results: DataFrame) -> List[float]:
    keys = results.keys()
    normalized_similarities: np.ndarray
    if "score" in keys:
        normalized_similarities = np.exp(results["score"] - np.max(results["score"]))
    elif "_distance" in keys:
        normalized_similarities = np.exp(-results["_distance"])
    else:
        normalized_similarities = np.linspace(1, 0, len(results))
    return normalized_similarities.tolist()

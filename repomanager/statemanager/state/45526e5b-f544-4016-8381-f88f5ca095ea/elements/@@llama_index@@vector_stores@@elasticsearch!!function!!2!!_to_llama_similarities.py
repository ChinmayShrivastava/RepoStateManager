def _to_llama_similarities(scores: List[float]) -> List[float]:
    if scores is None or len(scores) == 0:
        return []

    scores_to_norm: np.ndarray = np.array(scores)
    return np.exp(scores_to_norm - np.max(scores_to_norm)).tolist()

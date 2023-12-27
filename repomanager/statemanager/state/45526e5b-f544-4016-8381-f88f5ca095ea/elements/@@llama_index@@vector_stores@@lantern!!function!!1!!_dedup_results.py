def _dedup_results(results: List[DBEmbeddingRow]) -> List[DBEmbeddingRow]:
    seen_ids = set()
    deduped_results = []
    for result in results:
        if result.node_id not in seen_ids:
            deduped_results.append(result)
            seen_ids.add(result.node_id)
    return deduped_results

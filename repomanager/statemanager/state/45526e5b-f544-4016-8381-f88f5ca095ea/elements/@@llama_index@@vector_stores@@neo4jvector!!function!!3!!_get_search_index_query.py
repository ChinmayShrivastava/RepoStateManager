def _get_search_index_query(hybrid: bool) -> str:
    if not hybrid:
        return (
            "CALL db.index.vector.queryNodes($index, $k, $embedding) YIELD node, score "
        )
    return (
        "CALL { "
        "CALL db.index.vector.queryNodes($index, $k, $embedding) "
        "YIELD node, score "
        "WITH collect({node:node, score:score}) AS nodes, max(score) AS max "
        "UNWIND nodes AS n "
        # We use 0 as min
        "RETURN n.node AS node, (n.score / max) AS score UNION "
        "CALL db.index.fulltext.queryNodes($keyword_index, $query, {limit: $k}) "
        "YIELD node, score "
        "WITH collect({node:node, score:score}) AS nodes, max(score) AS max "
        "UNWIND nodes AS n "
        # We use 0 as min
        "RETURN n.node AS node, (n.score / max) AS score "
        "} "
        # dedup
        "WITH node, max(score) AS score ORDER BY score DESC LIMIT $k "
    )

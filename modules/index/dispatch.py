DEFAULT_DOCUMENT_CONTEXT_DISPATCH = {
    "get_unique_identifiers": False,
    "get_citations": False,
    "get_insights": False,
    "insight_engine": False,
    "chunk_engine": False,
    "persist": False,
}

DEFAULT_DOCUMENT_CONTEXT_DEPENDENCY_DISPATCH = {
    "get_unique_identifiers": [],
    "get_citations": ["get_unique_identifiers"],
    "get_insights": ["get_citations"],
    "insight_engine": ["get_insights"],
    "chunk_engine": ["get_insights"],
    "persist": ["insight_engine", "chunk_engine"],
}

def document_context_dependency_check(key, dispatch):
    for d in DEFAULT_DOCUMENT_CONTEXT_DEPENDENCY_DISPATCH[key]:
        assert dispatch[d]

def dispatch_next_step(obj, dispatch):
    vocab = {
        "get_unique_identifiers": obj._add_all_unique_identifiers,
        "get_citations": obj._add_all_citations,
        "get_insights": obj._generate_insights,
        "insight_engine": obj.add_vector_index,
        "chunk_engine": obj.add_vector_index,
        "persist": obj.persist,
    }
    order = [
        "get_unique_identifiers",
        "get_citations",
        "get_insights",
        "insight_engine",
        "chunk_engine",
        "persist",
    ]
    for k in order:
        if not dispatch[k]:
            vocab[k]()
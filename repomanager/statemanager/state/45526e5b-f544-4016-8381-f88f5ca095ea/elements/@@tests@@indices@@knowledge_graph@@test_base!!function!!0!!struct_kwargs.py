def struct_kwargs() -> Tuple[Dict, Dict]:
    """Index kwargs."""
    index_kwargs = {
        "kg_triple_extract_template": MOCK_KG_TRIPLET_EXTRACT_PROMPT,
    }
    query_kwargs = {
        "query_keyword_extract_template": MOCK_QUERY_KEYWORD_EXTRACT_PROMPT,
    }
    return index_kwargs, query_kwargs

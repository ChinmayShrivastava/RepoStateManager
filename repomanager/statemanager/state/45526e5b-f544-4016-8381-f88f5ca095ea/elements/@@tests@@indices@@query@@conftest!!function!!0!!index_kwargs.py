def index_kwargs() -> Dict:
    """Index kwargs."""
    return {
        "tree": {
            "summary_template": MOCK_SUMMARY_PROMPT,
            "insert_prompt": MOCK_INSERT_PROMPT,
            "num_children": 2,
        },
        "list": {},
        "table": {
            "keyword_extract_template": MOCK_KEYWORD_EXTRACT_PROMPT,
        },
        "vector": {},
        "pinecone": {},
    }

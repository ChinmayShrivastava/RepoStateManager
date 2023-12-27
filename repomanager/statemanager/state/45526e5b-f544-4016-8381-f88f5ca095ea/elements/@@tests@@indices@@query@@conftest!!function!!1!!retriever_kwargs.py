def retriever_kwargs() -> Dict:
    return {
        IndexStructType.TREE: {
            "query_template": MOCK_QUERY_PROMPT,
            "text_qa_template": MOCK_TEXT_QA_PROMPT,
            "refine_template": MOCK_REFINE_PROMPT,
        },
        IndexStructType.LIST: {},
        IndexStructType.KEYWORD_TABLE: {
            "query_keyword_extract_template": MOCK_QUERY_KEYWORD_EXTRACT_PROMPT,
        },
        IndexStructType.DICT: {
            "similarity_top_k": 1,
        },
        IndexStructType.PINECONE: {
            "similarity_top_k": 1,
        },
    }

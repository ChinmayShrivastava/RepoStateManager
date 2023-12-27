def struct_kwargs() -> Tuple[Dict, Dict]:
    """Index kwargs."""
    # NOTE: QuestionAnswer and Refine templates aren't technically used
    index_kwargs = {
        "schema_extract_prompt": MOCK_SCHEMA_EXTRACT_PROMPT,
        "output_parser": _mock_output_parser,
    }
    query_kwargs = {
        "text_qa_template": MOCK_TEXT_QA_PROMPT,
        "refine_template": MOCK_REFINE_PROMPT,
    }
    return index_kwargs, query_kwargs
